#This is for calibrating the SW 420 vibration sensor.
#Run this program while shaking the sensor; you might need to adjust the screw on the sensor to increase or decrease sensitivity.

from machine import Pin
import time

#Pin setup
vibration_sensor = Pin(22, Pin.IN)

#Global variables
vibration_count = 0

#Loop Until 6 vibrations detected then ends loop
while True:
    if vibration_sensor.value() == 1:
        print("Vibration detected!")
        time.sleep_ms(800)
        vibration_count = vibration_count + 1
        if vibration_count == 6:
            print("alarm trigger")
            break
    
# If no vibration is detected, print ellipses
    else:
        print("...")
        time.sleep_ms(800)
