
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
    
#define GPIO pins
GPIO_pins = (-1, -1, -1) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 24      	 # Direction -> GPIO Pin
step = 23      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


# call the function, pass the arguments
mymotortest.motor_go(False, "Full" , 1000, .001, True, .05)
GPIO.output(step, GPIO.LOW)
GPIO.output(direction, GPIO.LOW)
# good practise to cleanup GPIO at some point before exit
#GPIO.cleanup()
