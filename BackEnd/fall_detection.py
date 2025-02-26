import time
import math
from sense_hat import SenseHat
from twilio.rest import Client
from dotenv import load_dotenv
import os
import speech_recognition as sr  # For microphone input

# Load environment variables from the .env file
load_dotenv()

# Get Twilio Account SID and Auth Token from environment variables
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Check if the credentials are loaded correctly
if not account_sid or not auth_token:
    print("Error: ACCOUNT_SID and AUTH_TOKEN must be set in the .env file.")
    exit()

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Initialize Sense HAT
sense = SenseHat()
sense.set_imu_config(True, False, True)  # Enable accelerometer and gyroscope

# Define thresholds
ACCELERATION_THRESHOLD = 2.0  # Adjust based on experimentation
ROTATION_THRESHOLD = 1.0     # Adjust based on experimentation
DETECTION_WINDOW = 0.5       # Time window in seconds to detect a fall
NO_MOVEMENT_THRESHOLD = 10   # Seconds of no movement to trigger emergency
TEMPERATURE_THRESHOLD = 5    # Temperature in Celsius
TEMPERATURE_DURATION = 30    # Duration in minutes

# Variables to track the last time movement was detected
last_move_time = time.time()

# Variables to track the last time a message was sent
last_message_time = time.time()

# Variables to track temperature duration
temperature_start_time = None

# Send WhatsApp message function
def send_whatsapp_message(message_body):
    message = client.messages.create(
        body=message_body,
        from_='whatsapp:+14155238886',  # Twilio's sandbox WhatsApp number
        to='whatsapp:+447516755943'     # Replace with the recipient's WhatsApp number
    )
    print(f"Message SID: {message.sid}")

# Fall detection function
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
        # Update last movement time
        global last_move_time
        last_move_time = time.time()

        # Wait for a brief period to check for sustained acceleration
        time.sleep(DETECTION_WINDOW)
        accel = sense.get_accelerometer_raw()
        accel_magnitude = math.sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)
        if accel_magnitude > ACCELERATION_THRESHOLD:
            # Check if rotational change exceeds threshold
            rotation_magnitude = math.sqrt(gyro['x']**2 + gyro['y']**2 + gyro['z']**2)
            if rotation_magnitude > ROTATION_THRESHOLD:
                return True
    return False

# Check for no movement in the last 10 seconds
def check_no_movement():
    global last_move_time
    current_time = time.time()

    # If no movement has been detected for more than NO_MOVEMENT_THRESHOLD seconds
    if current_time - last_move_time > NO_MOVEMENT_THRESHOLD:
        return True
    return False

# Function to listen for a 'yes' or 'no' answer from the user using a microphone
def listen_for_answer(question, timeout=15):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening: {question}")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=timeout)
        try:
            response = recognizer.recognize_google(audio).lower()
            print(f"User said: {response}")
            if "yes" in response or "yeah" in response:
                return True
            elif "no" in response:
                return False
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("Could not request results; check your network connection.")
    return None

# Function to check temperature and send alert if below threshold for specified duration
def check_temperature():
    global temperature_start_time
    current_temperature = sense.get_temperature()

    if current_temperature < TEMPERATURE_THRESHOLD:
        if temperature_start_time is None:
            temperature_start_time = time.time()
        elif time.time() - temperature_start_time >= TEMPERATURE_DURATION * 60:
            print("Dangerous temperature conditions detected!")
            send_whatsapp_message('Warning: Temperature has been below 5°C for over 30 minutes.')
            temperature_start_time = None  # Reset the timer after sending the alert
    else:
        temperature_start_time = None  # Reset the timer if temperature is above threshold

# Main function that keeps the program running
def main():
    global last_message_time
    try:
        while True:
            # Only send messages if 10 minutes have passed since the last message
            if time.time() - last_message_time >= 600:
                if detect_fall():
                    print("Fall detected!")
                    send_whatsapp_message('Oh no Grandma has fallen down and needs help! Here is where they have fallen.')
                    last_message_time = time.time()  # Update the last message time

                if check_no_movement():
                    print("No movement detected for 10 seconds. Emergency!")
                    send_whatsapp_message('No movement detected for 10 seconds. Emergency situation.')
                    last_message_time = time.time()  # Update the last message time

                # Ask the user if they have fallen
                answer1 = listen_for_answer("Have you fallen?", timeout=15)
                if answer1 is None:
                    print("Assuming fall as no answer received.")
                    send_whatsapp_message('Emergency! No response to fall detection.')

                # Ask if they need help
                answer2 = listen_for_answer("Do you need help?", timeout=15)
                if answer2 is None:
                    print("Assuming need for help as no answer received.")
                    send_whatsapp_message('Emergency! No response to help request.')

            # Check temperature conditions
            check_temperature()

            time.sleep(0.1)  # Adjust based on desired sensitivity
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == '__main__':
    main()
