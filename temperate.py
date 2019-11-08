#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM) # set to Broadcom SOC channel

probe1 = 3
mintemp = 80
runtime = 10
tempin = 79

GPIO.setup(probe1, GPIO.OUT)

try:
        while True:
            
            if tempin >= mintemp:

                end = time.time() + runtime
                GPIO.output(probe1, GPIO.HIGH) # turn on pump
                
                while time.time() < end:
                    time.sleep(1)

            GPIO.output(probe1, GPIO.LOW) # turn off the pump

        time.sleep(1)


except KeyboardInterrupt:
    print("  Quit")

    # Reset GPIO settings
    GPIO.cleanup()

