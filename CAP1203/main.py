# PiicoDev Capacitive Touch Sensor CAP1203 demo code
# Read the touch sensor buttons and print the result

from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_Unified import sleep_ms # cross-platform-compatible sleep

touchSensor = PiicoDev_CAP1203(sensitivity=2,touchmode='multi')
touchSensor.setNoiseThresh(2)
touchSensor.setAvgSample(0)
touchSensor.sensorEnable(2)
while True:
    # Example: Display touch-pad statuses
    
    status = touchSensor.read()
    #raw = touchSensor.readDeltaCounts()
    print("Touch Pad Status: " + str(status[1]) + "  " + str(status[2]) + "  " + str(status[3]))
    #touchSensor.clearInt()
    sleep_ms(100)