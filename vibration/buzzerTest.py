import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

class Buzzer:
    def __init__(self):
        self.buzzer = 26
        
        GPIO.setup(self.buzzer, GPIO.OUT)

    def buzzerOn(self):
      #set software limit to max
        GPIO.output(self.buzzer, GPIO.HIGH)

    def buzzerOff(self):
        GPIO.output(self.buzzer, GPIO.LOW)


### debug ###
if __name__ == "__main__":
    buzzer = Buzzer()

    buzzer.buzzerOn()
    time.sleep(1)
    buzzer.buzzerOff()