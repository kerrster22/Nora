# Import necessary libraries to send an email
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Function to send an emergency email
def send_emergency_email(from_email, to_email, subject, message):
    # You need a special key from SendGrid to send emails. Replace this with your own key
    sendgrid_api_key = 'YOUR_SENDGRID_API_KEY'  # Get your SendGrid API key from SendGrid website
    
    # Create a SendGrid client using your API key
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    
    # Specify the 'from' email address (who the email is coming from)
    from_email = Email(from_email)  # Put your email address here
    
    # Specify the 'to' email address (who the email is going to)
    to_email = To(to_email)  # Put the emergency contact's email address here
    
    # Define the content of the email (this is the text of the email)
    content = Content("text/plain", message)  # The message is the body of the email
    
    # Create the email with all the necessary details (from, to, subject, and content)
    mail = Mail(from_email, to_email, subject, content)

    try:
        # Try sending the email using SendGrid
        response = sg.send(mail)
        # If it succeeds, print the success message and status code (to confirm the email is sent)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        # If there is an error, print the error message
        print(f"Error sending email: {e}")

# Example of how to use the function:
# Replace the email addresses and message with your own details
send_emergency_email(
    'from-email@example.com',  # Replace with your own email address
    'emergency-contact@example.com',  # Replace with the emergency contact's email address
    'Emergency Alert',  # Subject of the email
    'This is an emergency message!'  # The body of the email (the actual message you want to send)
)
