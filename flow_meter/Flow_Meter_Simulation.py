import random as r

def calculate_pulses(t: int) -> int:
    """
    Calculates the expected number of pulses based on the time interval
    Adds 2% error based on documentation
    Returns an integer number of expected pulses

    Average water flow should be about 5.68 to 8.33L/min
    1L = 450 pulses
    (flow/60) * t * 450 is the number of pulses in t seconds
    """
    flow = r.uniform(5.68, 8.33)  # Calculate a flow rate in the average range
    pulses = (flow/60) * t * 450
    error = pulses * 0.02  # Calculate percent error
    return round(r.uniform(pulses - error, pulses + error))  # Calculate an int within the error range


f = open("data.txt", "a")  # Open a file to append to
INTERVAL = 5  # Time (sec) to gather input from the flow meter before calculating flow rate

for i in range(0, 5):  # Use range to simulate any number instances
    count = 0  # Reset the pulse count
    f.write(f"[START]")  # Mark the start of the instance
    desired_count = calculate_pulses(INTERVAL)

    while count < desired_count:  # Generate pulses until the count reaches the desired value
        digit = r.randint(0, 1)
        if digit == 1:
            count += 1
            f.write("1")
        elif digit == 0:
            f.write("0")

    f.write(f"[END]\n")  # Mark the end of the instance
    rate = round(count / (7.5 * INTERVAL), 2)  # Calculate flow rate
    print(f"Liter/Min = {rate}")
    f.flush()  # Empty the buffer before the next instance

f.close()
