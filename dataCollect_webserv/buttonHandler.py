import RPi.GPIO as GPIO           # import RPi.GPIO module  
import time

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # set a port/pin as an input  
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set a port/pin as an output   

try:
    while(1):
        print(f"pin 10: {GPIO.input(10)} - pin 11: {GPIO.input(11)}")  
        time.sleep(0.1)

finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  