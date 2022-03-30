import RPi.GPIO as GPIO
import time


buzzer = 26
switch = 31

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

for i in range(5):
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
