#/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering


class IO:
    def __init__(self, motorClass=0):
        self.motorClass = motorClass

        self.SW1 = 9
        self.SW2 = 11
        self.SW3 = 25

        self.Button1 = 17
        self.Button2 = 27

        self.LED1 = 4
        self.LED2 = 19
        self.LED3 = 26

        GPIO.setup(self.Button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        GPIO.setup(self.Button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

        GPIO.setup(self.LED1, GPIO.OUT)
        GPIO.setup(self.LED2, GPIO.OUT)
        GPIO.setup(self.LED3, GPIO.OUT)

        GPIO.setup(self.SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        #GPIO.add_event_detect(self.Button1, GPIO.RISING, callback=self.Button1_callback, bouncetime=100)
        self.ok_time = time.time()

        self.interrupt_timeout = 3
        GPIO.add_event_detect(self.SW1, GPIO.RISING, callback=self.SW1_callback, bouncetime=400)

    def set_SW1_timeout(self, timeout): 
        self.interrupt_timeout = timeout

    def SW1_callback(self, channel):
        # Control loop if the device is already calibrated
        if(GPIO.input(self.SW1)==GPIO.LOW):
            # interrupt debounce
            if(time.time() > self.ok_time):
                self.motorClass.motor_stop()
                self.ok_time = time.time() + self.interrupt_timeout
        print("SW1 clicked")
    
    def readButton1(self):
        if(GPIO.input(self.Button1)==GPIO.HIGH):
            return 1
        else:
            return 0


if __name__ == "__main__":
    io = IO()
    while True:       
        #print(io.readButton1())
        GPIO.output(io.LED1, GPIO.HIGH)
        GPIO.output(io.LED2, GPIO.HIGH)
        GPIO.output(io.LED3, GPIO.HIGH)
