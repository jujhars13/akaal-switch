__version__ = 1.2

from src import display
from time import sleep
import RPi.GPIO as GPIO
import time
import os
import urllib.request
import http.client
import subprocess

http.client.HTTPConnection.debuglevel = 1

print("Starting Akaal Switch")

# constants
PIN_BUTTON = 36
PIN_AMP_POWER = 33

IFTTT_URL = os.getenv('IFTTT_URL')  # None
if IFTTT_URL is None:
    raise ValueError('IFTTT_URL not specified in env')

# Numbers pins by physical location
GPIO.setmode(GPIO.BOARD)

# GPIO PIN_BUTTON set up as input.
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# don't send +5v to the amp until we need it 'cos
# the speaker hisses all the time due to the
# low quality onboard PI DAC. So we'll only power up
# the amp when we need to - JIT
# 2020-07 amp is noisy and fiddly, going to ignore
# GPIO.setup(PIN_AMP_POWER, GPIO.OUT)
# GPIO.output(PIN_AMP_POWER, GPIO.LOW)

print(f"Waiting for falling edge on port {PIN_BUTTON}")
# now the program will do nothing until the signal on the pin
# starts to fall towards zero. This is why we used the pull-up
# to keep the signal high and prevent a false interrupt
# During this waiting time, your computer is not
# wasting resources by polling for a button press

try:
    while True:
        # interrupt, wait until true
        GPIO.wait_for_edge(PIN_BUTTON, GPIO.RISING)
        # if we're here, an edge was recognized
        sleep(0.005) # debounce for 5mSec
        # only show valid edges
        if GPIO.input(PIN_BUTTON) == 1:
            print(f"\n Button pressed {PIN_BUTTON}")
            display.renderDisplay()

            # # power up the amp
            # GPIO.output(PIN_AMP_POWER, GPIO.HIGH)
            # # # speak!
            # subprocess.run(
            #     ["/usr/bin/omxplayer", "/opt/akaal-switch/app/woof.wav"]
            # )
            # time.sleep(1)

            # call IFTTT
            print(f"Calling {IFTTT_URL}")
            res = urllib.request.urlopen(IFTTT_URL).read()
            print(f"IFTTT response: {res}")

            # power down the amp
            # GPIO.output(PIN_AMP_POWER, GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Akaal Switch")
