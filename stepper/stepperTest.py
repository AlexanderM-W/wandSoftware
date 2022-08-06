
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
from IO import IO
import time
    

class Stepper():    
    def __init__(self):


        #define GPIO pins
        self.GPIO_pins = (-1, -1, -1) # Microstep Resolution MS1-MS3 -> GPIO Pin
        self.direction = 24      	 # Direction -> GPIO Pin
        self.step = 23      # Step -> GPIO Pin

        self.up = 0
        self.down = 1
        self.maxSteps = 13000

        self.mymotortest = RpiMotorLib.A4988Nema(self.direction, self.step, self.GPIO_pins, "A4988")

    def moveStepper(self, up_or_down, steps):
        if(up_or_down == "up"):
            self.mymotortest.motor_go(self.up, "Full" , steps, .002, True, .05)
        elif(up_or_down == "down"):
            self.mymotortest.motor_go(self.down, "Full" , steps, .002, True, .05)

    def calibrate(self):
        self.mymotortest.motor_go(self.up, "Full" , 15000, .0008, True, .05)

    def setRest(self):
        GPIO.output(self.step, GPIO.LOW)
        GPIO.output(self.direction, GPIO.LOW)

    def mmToStep(self,mm):
        return int(mm*200)

if __name__ == "__main__":
    
    # Declare an named instance of class pass GPIO pins numbers
    stepper = Stepper()
    io = IO(stepper.mymotortest)

    stepper.calibrate()
    for i in range(100):
        stepper.moveStepper("down", stepper.mmToStep(0.02))
        time.sleep(0.1)
    stepper.moveStepper("up", stepper.mmToStep(5))
    stepper.setRest()
    # call the function, pass the arguments
    #mymotortest.motor_go(up, "Full" , 500, .002, True, .05)
    
