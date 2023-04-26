import RPi.GPIO as GPIO
from time import sleep

"""
Code for setting up the blue and red LEDs on a LED strip
"""

BLUE_LED = 31  # Blue LED pin
RED_LED = 32  # Red LED pin
GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode (Can also use BCM); Must be done
GPIO.setup(BLUE_LED, GPIO.OUT)  # Set BLUE_LED as output pin
GPIO.setup(RED_LED, GPIO.OUT)  # Set RED_LED as output pin
GPIO.output(BLUE_LED, True)  # Blue LED initially off
GPIO.output(RED_LED, True)  # Red LED initially off

def morse():  # Pulses LEDs in morse code (1/2 time)
    # W
    short_pulse()
    long_pulse()
    long_pulse()

    # D
    long_pulse()
    short_pulse()
    short_pulse()

    # S
    short_pulse()
    short_pulse()
    short_pulse()
    led_off()

def short_pulse():  # Pulses the LEDs for a short period of time
    led_blue()
    sleep(0.5)
    led_off()
    sleep(0.5)

def long_pulse():  # Pulses the LEDs for a long period of time
    led_blue()
    sleep(1.5)
    led_off()
    sleep(0.5)

def led_off():  # Turns both LED colors off
    GPIO.output(RED_LED, True)
    GPIO.output(BLUE_LED, True)

def led_red():  # Turns red LEDs on and blue off
    GPIO.output(RED_LED, False)
    GPIO.output(BLUE_LED, True)

def led_blue():  # Turns blue LEDs on and red off
    GPIO.output(RED_LED, True)
    GPIO.output(BLUE_LED, False)
