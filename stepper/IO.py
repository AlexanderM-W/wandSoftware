#/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
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

        GPIO.add_event_detect(self.Button1, GPIO.RISING, callback=self.Button1_callback, bouncetime=100)
        GPIO.add_event_detect(self.SW1, GPIO.RISING, callback=self.SW1_callback, bouncetime=100)

    def Button1_callback(self, channel):
        print("Button1 was pushed!")
        self.motorClass.motor_stop()
        while(GPIO.input(self.Button1) ==GPIO.HIGH):
            GPIO.output(self.LED1, GPIO.LOW)

    def SW1_callback(self, channel):
        print("endstop1 clicked")


if __name__ == "__main__":
    io = IO()


    

    while True: # Run forever

        
            
        
        GPIO.output(io.LED1, GPIO.HIGH)
        GPIO.output(io.LED2, GPIO.HIGH)
        GPIO.output(io.LED3, GPIO.HIGH)
