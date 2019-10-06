import RPi.GPIO as GPIO
import time
from subprocess import call
import os
import urllib.request

# our libs
from src import display

# constants
PIN_BUTTON = 36
PIN_LED = 37

print("Starting Akaal Switch")

IFTTT_URL = os.getenv('IFTTT_URL')  # None
if IFTTT_URL is None:
    raise ValueError('IFTTT_URL not specified in env')

# Numbers pins by physical location
GPIO.setmode(GPIO.BOARD)

# Set LED pin mode as output
GPIO.setup(PIN_LED, GPIO.OUT)
# Set LED pin to low(0V)
GPIO.output(PIN_LED, GPIO.LOW)
# GPIO PIN_BUTTON set up as input.
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print(f"Waiting for falling edge on port {PIN_BUTTON}")
# now the program will do nothing until the signal on the pin
# starts to fall towards zero. This is why we used the pull-up
# to keep the signal high and prevent a false interrupt
# During this waiting time, your computer is not
# wasting resources by polling for a button press

p = GPIO.PWM(PIN_LED, 1000)  # set LED Frequency to 1KHz


def pulseLed(pin):
    # pulse LED up and down

    pin.start(0)  # Start PWM output, Duty Cycle = 0
    for dc in range(0, 101, 3):   # Increase duty cycle: 0~100
        pin.ChangeDutyCycle(dc)     # Change duty cycle
        time.sleep(0.05)
    time.sleep(1)

    for dc in range(100, -1, -3):  # Decrease duty cycle: 100~0
        pin.ChangeDutyCycle(dc)
        time.sleep(0.05)
    time.sleep(1)


try:
    while True:
        # interrupt, wait until true
        # GPIO.wait_for_edge(PIN_BUTTON, GPIO.FALLING)
        print(f"\n Button pressed {PIN_BUTTON}")
        display.renderDisplay()
        req = urllib.request.Request(IFTTT_URL)
        pulseLed(p)
        p.stop()
        exit 1
except KeyboardInterrupt:
    p.stop()
    GPIO.output(PIN_LED, GPIO.HIGH)    # turn off all LEDs
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()
print("Stopping Akaal Switch")
