import time
import sys
import RPi.GPIO as GPIO

'''NOTE: Code from other resources is the same as in Flow_Meter_Code'''
global count  # Pulses counted in a specified interval
count = 0  # Initialize count to 0

# Try-except over entire code since the interrupt can happen while in count_increment() or in the while loop
try:
    def count_increment(FM_INPUT_PIN):  # Increments the pulse count
        global count
        count += 1


    CONSTANT = 7.5  # Constant value used to calibrate flow rate
    FM_INPUT_PIN = 13  # Using board pin 13 for input
    GPIO.setmode(GPIO.BOARD)  # Set pin reading to BOARD mode (Can also use BCM); Must be done
    GPIO.setup(FM_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the channel as an input

    # On rising edge call the count_increment function, bounce time set to 10ms
    GPIO.add_event_detect(FM_INPUT_PIN, GPIO.RISING, callback=count_increment, bouncetime=20)

    water_volume = float(input("How many liters of water are being poured?\n"))
    input("Press enter when ready to begin test and crtl+C to end the test")  # Pause until ready to start the test
    start_time = time.time()  # Time when the test started

    while True:
        pass  # Do nothing else while count is being incremented

except KeyboardInterrupt:
    stop_time = time.time()  # Time when the test ended
    interval = round(stop_time - start_time, 3)  # Time elapsed during the test in seconds
    count_rate = round(count / (CONSTANT * interval), 2)  # Flow rate using counts
    actual_rate = round(water_volume / (interval / 60), 2)  # Actual flow rate
    calibration_factor = actual_rate / count_rate  # Value needed to tune the constant
    print(f"\nOver {interval} seconds, {count} pulses were counted")
    print(f"Actual flow rate:   {actual_rate} L/min")
    print(f"Count flow rate:    {count_rate} L/min")
    print(f"Calibration factor: {calibration_factor}")
    print(f"The constant needed is {CONSTANT} * {calibration_factor} = {CONSTANT * calibration_factor}")
    GPIO.cleanup()
    sys.exit()
