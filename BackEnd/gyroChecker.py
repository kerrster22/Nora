import time
from sense_hat import SenseHat
import math

# Initialize Sense HAT
sense = SenseHat()
sense.set_imu_config(True, False, True)  # Enable accelerometer and gyroscope

# Define thresholds
ACCELERATION_THRESHOLD = 2.0  # Adjust based on experimentation
ROTATION_THRESHOLD = 1.0     # Adjust based on experimentation
DETECTION_WINDOW = 0.5       # Time window in seconds to detect a fall

def detect_fall():
    # Get accelerometer and gyroscope data
    accel = sense.get_accelerometer_raw()
    gyro = sense.get_gyroscope_raw()

    # Calculate acceleration magnitude
    accel_magnitude = math.sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)

    # Calculate rotational magnitude
    rotation_magnitude = math.sqrt(gyro['x']**2 + gyro['y']**2 + gyro['z']**2)

    # Check if acceleration exceeds threshold
    if accel_magnitude > ACCELERATION_THRESHOLD:
        # Wait for a brief period to check for sustained acceleration
        time.sleep(DETECTION_WINDOW)
        accel = sense.get_accelerometer_raw()
        accel_magnitude = math.sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)
        if accel_magnitude > ACCELERATION_THRESHOLD:
            # Check if rotational change exceeds threshold
            if rotation_magnitude > ROTATION_THRESHOLD:
                return True
    return False

try:
    while True:
        if detect_fall():
            print("Fall detected!")
            # Implement additional actions here (e.g., send alert)
        time.sleep(0.1)  # Adjust based on desired sensitivity
except KeyboardInterrupt:
    print("Program terminated.")
