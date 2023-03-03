import time
import sys
import RPi.GPIO as GPIO

'''NOTE: 
Code resources and how they were used is listed in the "Flow Meter Resource Links.txt" file
GPIO setup was detailed in the module documentation and all resources '''

global count  # Pulses counted in a specified interval
global enable
INTERVAL = 1  # Time (sec) to gather input from the flow meter

def count_increment(FM_INPUT_PIN):  # Increments the pulse count
    '''NOTE: Function format was the same/similar in every resource found'''
    global count
    global enable
    if enable == 1:
        count += 1
        print(f"Current count: {count}")


FM_INPUT_PIN = 13  # Using board pin 13 for input
GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode (Can also use BCM); Must be done
GPIO.setup(FM_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the channel as an input
# On rising edge call the count_increment function, bounce time set to 10ms for now
GPIO.add_event_detect(FM_INPUT_PIN, GPIO.RISING, callback=count_increment, bouncetime=10)

try:
    while True:
        print("starting loop")
        enable = 1
        count = 0  # Reset the count
        stop_time = time.time() + INTERVAL  # Time to stop counting pulses; current time + interval time
        while time.time() <= stop_time:  # Loop until the current time exceeds the stop time

            pass  # Do nothing else while count is being incremented

        # Calculate the rate after the interval has ended
        rate = round(count / (7.5 * INTERVAL), 2)
        print(f"\nCount: {count}")
        print(f"Liter/Min = {rate}\n\n")

        enable = 0
        print("pausing")
        time.sleep(3)  # Wait between instances

except KeyboardInterrupt:  # Exit after done testing the code
    print('\nkeyboard interrupt!')
    GPIO.cleanup()
    sys.exit()
