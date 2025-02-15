#THIS IS FOR TESTING/DEBUGGING YOUR SETUP

#Pico-Secure-Delivery-Box made by (woodycal @ github)(u/sac2727 @ reddit)
#The code for asynchronous-web-server-micropython by https://randomnerdtutorials.com/raspberry-pi-pico-w-asynchronous-web-server-micropython/

# Import necessary modules
import network
import socket
import time
import asyncio
import BME280
from machine import Pin, I2C


# Pin setup
led = Pin('LED', Pin.OUT)
vibration_sensor = Pin(22, Pin.IN)
relay_lock = Pin(14, Pin.OUT) #Note make sure to wire this correctly so if pico crashes it releases relay!
relay_siren = Pin(15, Pin.OUT)
box_sensor = Pin(12, Pin.IN, Pin.PULL_UP)# box sensor
box_sensor1 = Pin(13, Pin.IN, Pin.PULL_UP)# Sensor for pico enclosure

# Initialize I2C communication for bme280
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=10000) #For bme280 sensor

# Wi-Fi credentials
ssid = 'YOURSSID'
password = 'YOURPASSWORD'

# Initialize variables
state = "STARTUP"
weather_value = 0
vibrationcount = 0
startupcount = 0

# HTML template for the webpage
def webpage(weather_value, state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Secure Box Version 1.0</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Pico Secure Box</h1>
            <h2>Secure Box Controls</h2>
            <form action="./ARMED">
                <input type="submit" value="ARMED" />
            </form>
            <br>
            <form action="./DISARMED">
                <input type="submit" value="DISARMED MODE" />
            </form>
            <br>
            <form action="./DROPOFFMODE">
            <input type="submit" value="DROPOFFMODE" />
            </form>
            <br>
            <p style="color:DarkRed;">Secure Box Status: {state}</p>
            <h2>Fetch Weather Statistics</h2>
            <form action="./getweathervalue">
                <input type="submit" value="Fetch Weather Stats" />
            </form>
            <p>Weather Statisics: {weather_value}</p>
            <h2>Modes Explained</h2>
            <b style="color:DarkRed;">ARMED:</b><strong>      This mode locks the box and activates the alarm.<strong>
            <br>
            <b style="color:DarkRed;">DISARMED:</b><strong>      This mode disarms and unlocks the box (acts as service mode).<strong>
            <br>
            <b style="color:DarkRed;">DROPOFFMODE:</b><strong>      This mode waits for the box to be opened. Once opened, a 180-second timer activates, after which it is set to ARMED mode (locks box and activates alarm).<strong>
            <br>
            <p>For future updates, please check my GitHub page. <a href="https://github.com/woodycal/pico-secure-delivery-box">Here</a></p>
        </body>
        </html>
        """
    return str(html)

# Init Wi-Fi Interface
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

# Asynchronous functio to handle client's requests
async def handle_client(reader, writer):
    global state
    global dropboxvalue
    
    print("Client connected")
    request_line = await reader.readline()
    print('Request:', request_line)
    
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    print('Request:', request)
    
    # Process the request and update variables
    if request == '/ARMED?':
        print('ARMED ACTIVATED')
        state = 'ARMED'
    elif request == '/DISARMED?':
        print('DISARMED ACTIVATED')
        state = 'DISARMED'
    elif request == '/DROPOFFMODE?':
        print('DROPOFFMODE ACTIVATED')
        state = 'DROPOFFMODE'
        dropboxvalue = 0
        relay_lock.value(1)
    elif request == '/getweathervalue?':
        global weather_value
        bme = BME280.BME280(i2c=i2c)
        # Read sensor data
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        # Convert temperature to fahrenheit
        tempF = (bme.read_temperature()/100) * (9/5) + 32
        tempF = str(round(tempF, 2)) + 'F'
        weather_value = ("Temperature:", tempC, "Humidity:", hum, "Pressure:", pres)

    # Generate HTML response
    response = webpage(weather_value, state)  

    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')

#Logic for controlling box status modes
async def Boxstatus():
    global state
    global vibrationcount
    global startupcount
    if state == 'STARTUP':
        led.value(1)
        relay_siren.value(1)
        time.sleep(1)
        led.value(0)
        relay_siren.value(0)
        startupcount += 1
        if startupcount == 4:
            state = "DISARMED"
            print('Startup mode deactivated')
    elif state == 'ARMED':
        print('Box is Armed')
        relay_lock.value(0)
        if box_sensor.value() or box_sensor1.value() == 1:
            relay_siren.value(1)
            print('sensor value changed')
        elif vibration_sensor.value() == 1:
            print("Vibration detected!")
            vibrationcount += 1
            if vibrationcount == 6:
                print("alarm triggered")
                relay_lock.value(0)
                relay_siren.value(1)
    elif state == 'DISARMED':
            relay_siren.value(0)
            relay_lock.value(1)
            Print('Box is disarmed')
            time.sleep(2)
    elif state == 'DROPOFFMODE':
        print('Box is in dropoffmode')
        if box_sensor.value() or box_sensor1.value() == 1:
            print('Sensor was triggered in dropoffmode')
            time.sleep(180)
            print('Box is now armed')
            state = "ARMED"
            
                    
async def main():    
    if not init_wifi(ssid, password):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    
    while True:
        # Add other tasks that you might need to do in the loop
        await asyncio.sleep(5)
        asyncio.create_task(Boxstatus())
        print('This message will be printed every 5 seconds')
        

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
