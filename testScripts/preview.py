import time
import picamera
from gpiozero import PWMLED
from time import sleep
from picamera import PiCamera

import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)



def preview():
    camera = PiCamera()
    camera.resolution = (160, 160)
    GPIO.output(32, GPIO.HIGH) # Turn on    
    camera.start_preview()
    time.sleep(60)
    GPIO.output(32, GPIO.LOW)  # Turn off
    camera.stop_preview()
    return
preview()
