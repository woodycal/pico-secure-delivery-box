# Pico-Secure-Delivery-Box made by (woodycal @ github)(u/sac2727 @ reddit)
# Few issues with this i havent been able to pin point as of yet.
# 1. Their seems to be issue with npt time during start sometimes get an error, I assume its regarding connection as during testing i spammed and might have got blocked.
# 2. Their is an issue if you spam client (tkinter) it can cause tkinter to lock up and sometimes locks up server.
# I am unsure as of yet if this is down to async function in the server or an issue to do with tkinter (client) during testing or latency issue with wifi.
# Ideally some parts of this code should be in threads but it isnt widely supported as of yet in micropython.

# Import necessary modules
import asyncio
import network
import json
import socket
import time
import BME280
import ntptime
from machine import Pin, I2C

# Pin setup
led = Pin('LED', Pin.OUT)
vibration_sensor = Pin(22, Pin.IN)
relay_lock = Pin(14, Pin.OUT)  # Note make sure to wire this correctly so if pico crashes it releases relay!
relay_siren = Pin(15, Pin.OUT)
box_sensor = Pin(12, Pin.IN, Pin.PULL_UP)  # Box sensor
box_sensor1 = Pin(13, Pin.IN, Pin.PULL_UP)  # Sensor for pico enclosure

# Initialize I2C communication for bme280
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=10000)  # For BME280 sensor

# Wi-Fi credentials
ssid = ''
password = ''

# Initialize variables
state = "STARTUP"
weather_value = 0
vibrationcount = 0
startupcount = 0

# Global variables to store schedules
schedule1 = {}
schedule2 = {}
schedule3 = {}
schedule4 = {}

def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to your network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        print(wlan.status())
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        print('Failed to connect to Wi-Fi')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True
    
async def handle_client(reader, writer):
    global state, weather_value, schedule1, schedule2, schedule3, schedule4
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode().strip()
        print(f"Received \"{message}\" from {writer.get_extra_info('peername')}")
        
        if message == 'ARMED':
            state = 'ARMED'
            print(f"Send: {state!r}")
            writer.write(state.encode())
            await writer.drain()
            print("Close the connection")
            writer.close()
            writer.wait_closed()
        elif message == 'DISARMED':
            state = 'DISARMED'
            dropboxvalue = 0
            relay_lock.value(1)
            print(f"Send: {state!r}")
            writer.write(state.encode())
            await writer.drain()
            print("Close the connection")
            writer.close()
            writer.wait_closed()
        elif message == 'DROPOFFMODE':
            state = 'DROPOFFMODE'
            dropboxvalue = 0
            relay_lock.value(1)
            print(f"Send: {state!r}")
            writer.write(state.encode())
            await writer.drain()
            print("Close the connection")
            writer.close()
            writer.wait_closed()
        elif message == 'getweathervalue':
            weather_value = "Example Weather Value"
            print(f"Send: {weather_value!r}")
            writer.write(weather_value.encode())
            await writer.drain()
            print("Close the connection")
            writer.close()
            writer.wait_closed()
        elif message.startswith('schedule'):
            schedule_data = parse_schedule(message)
            if schedule_data:
                store_schedule(schedule_data)
                print(f"Stored schedule: {schedule_data}")
        elif message.startswith('GETSTATE'):
            print(f"Send: {state!r}")
            writer.write(state.encode())
            await writer.drain()
            print("Close the connection")
            writer.close()
            writer.wait_closed()
        elif message.startswith('CLEARSCHEDULES'):
            schedule1 = {}
            schedule2 = {}
            schedule3 = {}
            schedule1 = {}
        else:
            print(f"Unknown command: {message}")
            
def parse_schedule(message):
    # Extract the JSON part from the message
    try:
        start_index = message.find('{')
        end_index = message.rfind('}') + 1
        if start_index == -1 or end_index == 0:
            raise ValueError("No valid JSON found in the message.")
        
        json_data = message[start_index:end_index]
        print(f"Extracted JSON: {json_data}")  # Debugging line
        
        return json.loads(json_data)
    except (ValueError, IndexError) as e:
        print(f"Failed to parse schedule: {e}")
        return None

def store_schedule(schedule_data):
    global schedule1, schedule2, schedule3, schedule4
    # Extract the schedule number from the schedule key
    schedule_number = int(schedule_data.get('schedule', '').split()[1])
    
    # Store the schedule data in the corresponding global variable
    if schedule_number == 1:
        schedule1 = schedule_data
    elif schedule_number == 2:
        schedule2 = schedule_data
    elif schedule_number == 3:
        schedule3 = schedule_data
    elif schedule_number == 4:
        schedule4 = schedule_data
    else:
        print(f"Invalid schedule number: {schedule_number}")
 
async def Boxstatus():
    global state, vibrationcount, startupcount
    print(state)
    if state == 'STARTUP':
        led.value(1)
        relay_siren.value(1)
        time.sleep(2)
        led.value(0)
        relay_siren.value(0)
        startupcount += 1
        print(startupcount)
        if startupcount == 4:
            state = "DISARMED"
    elif state == 'ARMED':
        relay_lock.value(0)
        vibrationcount = 0
        if box_sensor.value() or box_sensor1.value() == 1:
            print("alarm activated")
            relay_siren.value(1)
            state = "TAMPER"
        elif vibration_sensor.value() == 1:
            vibrationcount += 1
            if vibrationcount == 6:
                relay_lock.value(0)
                relay_siren.value(1)
                state = "TAMPER"
    elif state == 'DISARMED':
        relay_siren.value(0)
        relay_lock.value(1)
        time.sleep(2)
    elif state == 'DROPOFFMODE':
        if box_sensor.value() or box_sensor1.value() == 1:
            time.sleep(180)
            state = "ARMED"
    elif state == 'TAMPER':
        relay_lock.value(0)
        relay_siren.value(1)

# Handles the schedule function that checks stored schedules
async def schedules():
    global schedule1, schedule2, schedule3, schedule4, state
    current_time = "{:02d}:{:02d}".format(time.localtime()[3], time.localtime()[4])
    print(f"Current Time: {current_time}")
    
    # List of schedules to check
    schedule_list = [schedule1, schedule2, schedule3, schedule4]
    print(schedule1)
    print(schedule2)
    print(schedule3)
    print(schedule4)
    
    for schedule in schedule_list:
        if not schedule:
            continue
        
        scheduled_hour = schedule.get("hour")
        scheduled_minute = schedule.get("minute")
        state_from_schedule = schedule.get("state")
        
        # scheduled time in HH:MM format
        scheduled_time = f"{scheduled_hour}:{scheduled_minute}"
        
        if current_time == scheduled_time:
            print(f"Time match at {current_time}, State: {state_from_schedule}")
            
            state1 = state_from_schedule
            
            if state1 == "ARMED":
                state = 'ARMED'
                print("System ARMED")
            elif state1 == "DISARMED":
                state = 'DISARMED'
                print("System DISARMED")
            elif state1 == "DROPOFFMODE":
                state = 'DROPOFFMODE'
                print("System in DROPOFFMODE")
            else:
                print("Unknown state")



async def main():
    if not init_wifi(ssid, password):
        return
    
    # Update time from npt server # refer to top theirs a bug here
    ntptime.settime()
    thetime = time.localtime()
    print(thetime)

    # Start the server and run the event loop
    server = asyncio.start_server(handle_client, "0.0.0.0", 8080)
    asyncio.create_task(server)
    print("starting servers")

    while True:
        # other tasks in loop
        await asyncio.sleep(5)
        asyncio.create_task(Boxstatus())
        asyncio.create_task(schedules())
        
        


# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()

except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
        
