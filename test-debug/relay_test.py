# THIS IS FOR TESTING RELAYS
# You will hear them click to signal a change.
# Make sure you wire the external circuit up correctly so that if they are powered, the lock is either on or off. 

# Import necessary modules
import time
from machine import Pin
# Pin setup
relay_lock = Pin(14, Pin.OUT) #Note make sure to wire this correctly so if pico crashes it releases relay!
relay_siren = Pin(15, Pin.OUT)

startupcount = 0

# set inital relay values
relay_lock.value(0)
relay_siren.value(0)

while True:
    print('starting up relays')
    time.sleep(1)
    relay_lock.value(1)
    print('relay_lock activated')
    time.sleep(1)
    relay_siren.value(1)
    print('relay_siren activated')
    time.sleep(1)
    relay_lock.value(0)
    time.sleep(1)
    print('relay_lock deactivated')
    time.sleep(1)
    relay_siren.value(0)
    print('relay_siren deactivated')
    time.sleep(1)
    startupcount += 1
    if startupcount == 2:
        print('startupcount hit 2 program close')
        time.sleep(5)
        break
