# PiicoDev Capacitive Touch Sensor CAP1203 demo code
# Read the touch sensor buttons and print the result

from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_CAP1203 import sleep_ms
#from PiicoDev_Unified import sleep_ms # cross-platform-compatible sleep
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)

frontSensor = PiicoDev_CAP1203(bus=5,sensitivity=1,touchmode='single')
backSensor = PiicoDev_CAP1203(bus=1,sensitivity=1,touchmode='single')
time.sleep(1)
frontSensor.setNoiseThresh(0)
frontSensor.setAvgSample(1)
frontSensor.sensorEnable(1)
frontSensor.setPowerButton(0)
frontSensor.powerButtonConf(0)
frontSensor.setRepeatRate(0)

backSensor.setNoiseThresh(0)
backSensor.setAvgSample(1)
backSensor.sensorEnable(1)
backSensor.setPowerButton(0)
backSensor.powerButtonConf(7) # Only generates an interrupt/output after 2.24s. see p. 44 
backSensor.setRepeatRate(0)


while True:
    status_frontSensor = frontSensor.read()
    status_backSensor = backSensor.read()
    print("Front touchpad: " + str(status_frontSensor[1]) + " // Back touchpad: " + str(status_backSensor[1]))
    frontSensor.clearInt()
    backSensor.clearInt()
    sleep_ms(150)
