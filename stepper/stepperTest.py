
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
from IO import IO
import time
import signal
    

class Stepper():    
    def __init__(self):
        #define GPIO pins
        self.GPIO_pins = (-1, -1, -1) # Microstep Resolution MS1-MS3 -> GPIO Pin
        self.direction = 24      	 # Direction -> GPIO Pin
        self.step = 23      # Step -> GPIO Pin
        self.enable = 14
        GPIO.setup(self.enable, GPIO.OUT)

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
        self.mymotortest.motor_go(self.down, "Full", 2000, 0.001, True, 0.05)
        self.mymotortest.motor_go(self.up, "Full" , 15000, .0008, True, .05)

    def setRest(self):
        #GPIO.output(self.step, GPIO.LOW)
        #GPIO.output(self.direction, GPIO.LOW)
        self.disableStepper()

    def mmToStep(self,mm):
        return int(mm*200)

    def enableStepper(self):
        GPIO.output(self.enable, GPIO.LOW)

    def disableStepper(self):
        GPIO.output(self.enable, GPIO.HIGH)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        stepper.setRest()
        exit(1)
 
signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    
    # Declare an named instance of class pass GPIO pins numbers
    stepper = Stepper()
    io = IO(stepper.mymotortest)
    while(1):
        if(io.readButton1()):
            stepper.calibrate()
    #stepper.moveStepper("down", stepper.mmToStep(5))
    #stepper.setRest()
    # call the function, pass the arguments
    #mymotortest.motor_go(up, "Full" , 500, .002, True, .05)
    
