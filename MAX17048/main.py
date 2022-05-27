import os
import sys
sys.path.append('../')
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from MAX17048 import DFRobot_MAX17043
import RPi.GPIO as GPIO

gauge = DFRobot_MAX17043()

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.IN)

def interruptCallBack(channel):
  gauge.clear_interrupt()
  print('Low power alert interrupt!')
  #put your battery low power alert interrupt service routine here
  
#GPIO.add_event_detect(7, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5)

rslt = gauge.begin()

while rslt != 0:
  print('gauge begin faild')
  time.sleep(2)
  rslt = gauge.begin()

#gauge.set_interrupt(32) #use this to modify alert threshold as 1% - 32% (integer)
print('gauge begin successful')
  
while True:
  time.sleep(2)
  print('voltage: ' + str(gauge.read_voltage()) + 'mV')
  print('percentage: ' + str(round(gauge.read_percentage(), 2)) + '%')
