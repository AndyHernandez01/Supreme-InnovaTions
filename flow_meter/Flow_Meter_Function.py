import time
import RPi.GPIO as GPIO

'''NOTE: Code from other resources is the same as in Flow_Meter_Code'''
INTERVAL = 1  # Time (sec) to gather input from the flow meter
FM_INPUT_PIN = 13  # Using board pin 13 for input
GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode (Can also use BCM); Must be done
GPIO.setup(FM_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the channel as an input

global count  # Pulses counted in a specified interval

def count_increment(FM_INPUT_PIN):  # Increments the pulse count
    global count
    count += 1


def get_flow_rate() -> float:  # Tallies the counts in an interval and calulates flow rate
    global count
    count = 0  # Reset the pulse count
    stop_time = time.time() + INTERVAL  # Time to stop counting pulses
    while time.time() <= stop_time:  # Loop until the current time exceeds the stop time
        pass  # Do nothing else while count is being incremented
    return round(count / (7.5 * INTERVAL), 2)  # Return flow rate


# On rising edge call the count_increment function, bounce time set to 10ms for now
GPIO.add_event_detect(FM_INPUT_PIN, GPIO.RISING, callback=count_increment, bouncetime=10)

print(f"Rate = {get_flow_rate()} L/min")  # Call get_flow_rate() and print the rate
GPIO.cleanup()
