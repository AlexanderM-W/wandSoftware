
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
from IO import IO
import time
import signal

#currentHeight = 0


class Stepper():
    def __init__(self):
        # define GPIO pins
        self.currentHeight = 0.0
        # Microstep Resolution MS1-MS3 -> GPIO Pin
        self.GPIO_pins = (-1, -1, -1)
        self.direction = 24      	 # Direction -> GPIO Pin
        self.step = 23      # Step -> GPIO Pin
        self.enable = 14
        GPIO.setup(self.enable, GPIO.OUT)

        self.up = 1
        self.down = 0
        self.maxSteps = 11000

        self.mymotortest = RpiMotorLib.A4988Nema(self.direction, self.step, self.GPIO_pins, "A4988")



    def moveStepper(self, up_or_down, steps):
        steps = int(steps)
        self.enableStepper()
        if(up_or_down == "up"):
            self.currentHeight -= self.steps2mm(steps)
            self.mymotortest.motor_go(self.up, "Full", steps, .0008, False, .05)
        elif(up_or_down == "down"):
            if(self.getCurrentHeight_mm() + self.steps2mm(steps) > self.steps2mm(self.maxSteps)):
                raise Exception("The target is out of range")

            self.currentHeight += self.steps2mm(steps)
            self.mymotortest.motor_go(self.down, "Full", steps, .0008, False, .05)
        self.disableStepper()

    def calibrate(self):
        self.currentHeight = 0.0
        self.enableStepper()
        self.mymotortest.motor_go(self.down, "Full", 1800, 0.0008, False, 0.05)
        self.mymotortest.motor_go(self.up, "Full", 15000, 0.0008, False, .05)
        self.mymotortest.motor_go(self.down, "Full", 100, 0.0008, False, 0.05)
        self.disableStepper()

        print("Calibration completed")

    def setRest(self):
        #GPIO.output(self.step, GPIO.LOW)
        #GPIO.output(self.direction, GPIO.LOW)
        self.disableStepper()

    def mm2steps(self, mm):
        return (mm*200.0)

    def steps2mm(self, steps):
        return (steps*1/200.0)

    def enableStepper(self):
        GPIO.output(self.enable, GPIO.LOW)

    def disableStepper(self):
        GPIO.output(self.enable, GPIO.HIGH)

    def getCurrentHeight_mm(self):
        return self.currentHeight

    def go2pose_mm(self, pose_mm):
        if(self.getCurrentHeight_mm() > float(pose_mm)):
            self.moveStepper("up", self.mm2steps(self.getCurrentHeight_mm() - pose_mm))
        elif(self.getCurrentHeight_mm() < float(pose_mm) ):
            self.moveStepper("down", self.mm2steps(pose_mm - self.getCurrentHeight_mm()) )
        else:
            return 0

    def motorStop(self):
        self.mymotortest.motor_stop()
        
def handler(signum, frame):
    print("Goodbye")
    stepper.setRest()
    exit(1)


signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":

    stepper = Stepper()
    io = IO(stepper)
    while(1):
        if(io.readButton1()):
            
            stepper.calibrate()
            #print(stepper.currentHeight)
            #stepper.moveStepper("down", stepper.mm2steps(5))
            #print(stepper.currentHeight)
            #stepper.moveStepper("up", stepper.mm2steps(2))
            #print(stepper.currentHeight)
            #stepper.go2pose_mm(3.5)
            #print(stepper.currentHeight)
