import wiringpi, time

def reset_pins(io):
    io.pinMode(26,io.OUTPUT)
    io.digitalWrite(26, io.LOW)


def pwm_dimm(io):
    STEP = 8
    pin = 26 # only supported on this pin
    io.pinMode(pin,io.PWM_OUTPUT)
    io.pwmWrite(pin, 500)


io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

try:
    reset_pins(io)    
    pwm_dimm(io)
    time.sleep(5)

except (KeyboardInterrupt, SystemExit):
    reset_pins(io)
