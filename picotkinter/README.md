# Pico Secure Delivery Box
![Setup guide](/Building-box/tkinterscreenshot.png)

## Item list:

### Raspberry Pi Pico W or Pico 2W (Needs WiFi)

### 2x Relay modules

### 1x SW 420 vibration sensor

### 1x BME 280 Temperature, Pressure, Humidity Sensor

### 2x Magnetic Door Contact Reed Switches

### 1x 12V Electric Drop Bolt Lock

### 1x 12V Siren

### 1x 12V Battery or power supply

Software: Micropython version 1.25.0 (https://micropython.org/download/RPI_PICO2_W/) and Thonny for uploading the following files to the Pico (main.py bme280.py and npttime.py)

## INSTRUCTIONS

### Upload
main.py BME280.py and npttime.py to the pico 2 w

### main.py
In main.py, please enter your Wi-Fi credentials. Please note that because the Pico W uses ntptime.py during startup to fetch the current time, you will need to allow access to the internet.

### picoclient.py
In picoclient.py, you will need to enter the host IP address of the Pico W on your local network. It should look
something like 192.168.0.2 (as shown by your router). Remember that if you change port numbers, you will need to
adjust them in both main.py and picoclient.py. 

**VERY IMPORTANT:** This will only work on normal Python. It will not work on MicroPython due to the limited libraries it has. 

This client works best on a raspberry pi with a touchscreen of some kind.

## Tkinter usage instructions
### Left side buttons
- **Armed**: Button sends a command to set the box in ARMED mode.
- **Disarmed**: Button sends a command to set the box in DISARMED mode.
- **Dropoffmode**: Button sends a command to set the box in DROPOFFMODE mode.
- **Weatherstatistics**: Button sends a command to set GETWEATHERSTATS mode (Gets current weather stats).
- **Get Box Status**: Gets the current state of the box if it's ARMED, DISARMED, DROPOFFMODE, or rarely STARTUP during booting process.

### Right side schedule
The way the schedule works is as follows:
1. Select your time, mode, and very importantly, the schedule number before submitting.
2. It will store these server-side, so if you send two schedule 1s, the last schedule 1 you send will update with the new parameters.
3. There is a maximum of 4 schedules that can be set, and these are permanent unless you press the "Clear Schedules" button or for some reason the Pico soft resets.

### Current issues
There are some issues I haven't yet managed to pinpoint, which cause sometimes the Tkinter app to lock up or the
Pico server. I haven't managed yet to find out what is causing it. It could be related to the way async works on
the server, which really needs to be threaded but isn't widely supported on MicroPython. Or it could be related to
the Tkinter app, I can't really figure it out at the moment as it seems to be both that are causing the issue.

There is also an issue with ntptime.py, which I believe during testing was because I was spamming their servers,
and either got a temporary ban or ran into request limits per minute.



