import time
import RPi.GPIO as GPIO
from bluedot.btcomm import BluetoothClient
import random
import sys


""" Combines the bluetooth client and flow meter code """
"""===================================VARIABLES==================================="""
"""Global Variables"""
global count  # Pulses counted in FM_INTERVAL seconds
count = 0  # Initialize count as an integer
"""Interval Variables"""
FM_INTERVAL = 1  # Seconds to gather input from the flow meter
BT_INTERVAL = 2  # Seconds between sending messages to the server
"""GPIO Variables"""
FM_INPUT_PIN = 13  # Using board pin 13 for input
GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode
GPIO.setup(FM_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set FM_INPUT_PIN as an input
"""Bluetooth variables"""
SERVER_NAME = "Biosure WDS"  # Name of the server to connect to
send_time = 0.0  # Initialize when to send the message to the server

"""===================================FUNCTIONS==================================="""
"""Flow Meter Functions"""
def count_increment(FM_INPUT_PIN):  # Increments the pulse count for the flow rate
    global count
    count += 1

def get_flow_rate() -> float:  # Tallies the counts in an interval and calculates flow rate
    global count
    count = 0  # Reset the pulse count
    stop_time = time.time() + FM_INTERVAL  # Time to stop counting pulses
    while time.time() <= stop_time:  # Loop until the current time exceeds the stop time
        pass  # Do nothing else while count is being incremented
    return round(count / (7.5 * FM_INTERVAL), 2)  # Return flow rate

def get_ozone_concentration(flow_rate):  # Calculates O3 concentration based on flow rate
    """
    From the manual: At 750 LPH -> 0.2 ppm and At 1500 LPH -> 0.4 ppm
    Assuming a linear relationship between flow rate and ppm
    With ppm (mg/L) on x-axis and flow (L/hr) on y-axis
    flow = ppm * slope; where slope is 3750.0

    First get ppm from flow rate:
    ppm (mg/L) = (Flow (L/min) * 60min/hr) / 3750 (L^2 / hr*mg)

    Then get O3 from flow and ppm
    O3 produced (mg/hr) = flow (L/min) * 60min/1hr * O3 dosage (mg/L)

    returns O3 concentration in mg/hr
    """
    ppm = (flow_rate * 60) / 3750.0
    return round(flow_rate * 60 * ppm, 2)


"""===================================MAIN CODE==================================="""
GPIO.add_event_detect(FM_INPUT_PIN, GPIO.RISING, callback=count_increment, bouncetime=10)  # Set function to call for pulse count
c = BluetoothClient(SERVER_NAME, data_received_callback=None, auto_connect=False)  # Set up server to connect to
f = open("/home/wds/error_file.txt", "w")  # Create a file to send errors to
f.close()
i, j = 1, 1  # Indexing for errors
allow_ending = False  # Allows for ending the program after a set amount of time
program_end_time = time.time() + 120  # Time limit for the program, so it doesn't run forever at boot-up
print("Program started, waiting for connection")

while True:  # main loop
    try:
        if not c.connected:  # Try to connect to the server if not already connected
            c.connect()
            print(f"Connected to {SERVER_NAME}")
            send_time = time.time() + BT_INTERVAL  # Initialize when to send the Bluetooth message
    except OSError:  # If unable to connect to server in time (About 5 sec), write error to a file and continue
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f = open("/home/wds/error_file.txt", "a")
        f.write(f"{exc_obj} time {i}\n")
        i += 1
        f.close()
        c.disconnect()

    try:  # Do calculations and send data to the server
        if time.time() >= send_time and c.connected:  # When connected to the server and BT_INTERVAL has passed
            print(f"Getting flow rate for {FM_INTERVAL} second(s)")
            rate = get_flow_rate()  # Get flow rate from flow meter
            print(f"Sending {rate} L/min to the tft\n")

            ozone = get_ozone_concentration(rate)  # Calculate O3 concentration using flow rate
            print(f"Sending {ozone} mg/hr to the tft\n")
            c.send(f"{rate} {ozone}")  # Send data to the server

            send_time = time.time() + BT_INTERVAL  # Update the time to send the next Bluetooth message

        if time.time() > program_end_time and allow_ending:  # If enabled, end the program after a set time
            GPIO.cleanup()
            break
    except OSError: # If an error sending data happens, write the error to a file and disconnect to so connecting can be done again
        """ NOTE:
        For some reason this error happens the very first time a message is sent to the TFT
        Only happens when code is run at boot on the Pi
        After reconnecting, the error never happens again
        """
        f = open("/home/wds/error_file.txt", "a")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        f.write(f"{exc_obj} time {j} at line {line_number}\n")
        j += 1
        f.close()
        c.disconnect()
