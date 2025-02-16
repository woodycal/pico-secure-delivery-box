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
In main.py please enter your Wi-Fi credentials, Please note that because the pico 2 w uses npttime.py during startup to fetch current time you will need to allow access to the internet.

### picoclient.py
In picoclient.py you will need to enter the host ip address of the pico 2 w on your local network, It should look like something 192.168.0.2 from your router. 
Remeber if you change port numbers you will need to adjust them in both main.py and picoclient.py
Also VERY IMPORTANT this will only work on normal python, It will not work on micropython due to the limited libraries it has.

### Current issues
Their is some issues i havent yet managed to pin point which causes sometimes the tkinter app to lock up or the pico server. I havent managed yet to find out what is doing it, It could be related to the way async works on the server which really needs to be threaded but isnt widely supported on micropython. Or it could be related to tkinter app i cant really figure it out atm as it seems to be both thats doing it.




