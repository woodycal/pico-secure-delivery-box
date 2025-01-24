#THIS IS FOR TESTING DOOR CONTACT SENSORS
#Please make sure depending on type sensor you have its wired correctly
#Some sensors are 2 way meaning they can have 3 wire points
#The style I had has 3 wire points
#You will need to wire both end points and leave the middle wire point redunant
#Pulling the two parts apart will trigger value == 1

#Import necessary modules
import time
from machine import Pin

#Pin setup
box_sensor = Pin(12, Pin.IN, Pin.PULL_UP)
box_sensor1 = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    if box_sensor.value() == 1:
        print('box_sensor was triggered')
        time.sleep(2)
    elif box_sensor1.value() == 1:
        print('box_sensor1 was triggered')
        time.sleep(2)
    else:
        print('Waiting ...')
        time.sleep(2)
