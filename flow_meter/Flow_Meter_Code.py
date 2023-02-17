import time
import sys
import RPi.GPIO as GPIO

'''NOTE: 
Code resources and how they were used is listed in the "Flow Meter Resource Links.txt" file
GPIO setup was detailed in the module documentation and all resources '''
FM_INPUT_PIN = 13  # Using board pin 13 for input
GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode (Can also use BCM); Must be done
GPIO.setup(FM_INPUT_PIN, GPIO.IN)  # Set up the channel as an input

global count  # Pulses counted in a specified interval
INTERVAL = 5  # Time (sec) to gather input from the flow meter

def count_increment(FM_INPUT_PIN):  # Increments the pulse count
    '''NOTE: Function format was the same/similar in every resource found'''
    global count
    count += 1


# On rising edge call the count_increment function, bounce time set to 10ms for now
GPIO.add_event_detect(FM_INPUT_PIN, GPIO.RISING, callback=count_increment, bouncetime=10)

while True:
    count = 0  # Reset the pulse count
    stop_time = time.time() + INTERVAL  # Time to stop counting pulses; current time + interval time

    while time.time() <= stop_time:  # Loop until the current time exceeds the stop time
        ''' NOTE:
        This method allows for printing/writing the input reading in real time
        The time method and printing idea came from https://www.youtube.com/watch?v=wpenAP8gN3c
        If reading the input is not necessary, a enable-sleep-disable method can be used '''
        try:
            print(GPIO.input(FM_INPUT_PIN), end="")  # Reads the value of the pin and prints it
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            GPIO.cleanup()
            sys.exit()

    # Calculate the rate after the interval has ended
    rate = round(count / (7.5 * INTERVAL), 2)
    print(f"Liter/Min = {rate}\n\n")
    time.sleep(1)
