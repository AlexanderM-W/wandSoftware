# PiicoDev Capacitive Touch Sensor CAP1203 demo code
# Read the touch sensor buttons and print the result

from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_CAP1203 import sleep_ms
#from PiicoDev_Unified import sleep_ms # cross-platform-compatible sleep
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)

touchSensor = PiicoDev_CAP1203(bus=5,sensitivity=1,touchmode='single')
time.sleep(1)
touchSensor.setNoiseThresh(0)
touchSensor.setAvgSample(1)
touchSensor.sensorEnable(1)
touchSensor.setPowerButton(0)
touchSensor.powerButtonConf(0)
touchSensor.setRepeatRate(0)


while True:
    # Example: Display touch-pad statuses
    
    status = touchSensor.read()
    #status = touchSensor.readDeltaCounts()
    print("Touch Pad Status: " + str(status[1]) + "  " + str(status[2]) + "  " + str(status[3]))
#    print("GPIO no " + str(7) + ": " + str(GPIO.input(7)))
#    print(touchSensor.getInt())
    touchSensor.clearInt()
    sleep_ms(300)
