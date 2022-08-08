
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
        self.enableStepper()
        if(up_or_down == "up"):
            self.mymotortest.motor_go(self.up, "Full" , steps, .002, False, .05)
        elif(up_or_down == "down"):
            self.mymotortest.motor_go(self.down, "Full" , steps, .002, False, .05)
        self.disableStepper()

    def calibrate(self):
        self.enableStepper()
        self.mymotortest.motor_go(self.down, "Full", 1800, 0.0008, False, 0.05)
        self.mymotortest.motor_go(self.up, "Full" , 15000, 0.0008, False, .05)
        self.disableStepper()

        print("Calibration completed")

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
    print("Goodbye")
    stepper.setRest()
    exit(1)
 
signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":

    stepper = Stepper()
    io = IO(stepper.mymotortest)
    while(1):
        if(io.readButton1()):
            stepper.calibrate()
            stepper.moveStepper("down", stepper.mmToStep(5))
    
