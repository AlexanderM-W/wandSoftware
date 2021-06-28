import RPi.GPIO as GPIO
import time

#ledpin = 32
butpin = 10
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system

GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(ledpin,GPIO.OUT)
#pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
#pi_pwm.start(0)				#start PWM of required Duty Cycle 
while True:

    if GPIO.input(butpin) == GPIO.LOW:
        print("LED is on")
    else:
        print("LED is off")

    time.sleep(0.5)
