from djoser.email import ActivationEmail
from django.core.mail import send_mail
import random


def generate_activation_code():
    """
    Generates a random 6-digit activation code.
    """
    return str(random.randint(100000, 999999))


def send_activation_email(email, activation_code):
    """
    Sends the activation code to the user's email address.
    """
    subject = "Your Activation Code"
    message = f"Your activation code is: {activation_code}"

    # Send the email using Django's email backend
    send_mail(
        subject,  # Subject of the email
        message,  # Body of the email
        'no-reply@example.com',  # From email (set to your actual from email)
        [email],  # To email (the user's email)
        fail_silently=False,  # Will raise an error if sending fails
    )


class CustomActivationEmail(ActivationEmail):
    """
    Custom email class that overrides Djoser's ActivationEmail.
    This class is used to send a unique activation code to the user.
    """
    template_name = "email/activation_code.html"  # Optional: If you use a template for the email body

    def send(self, user):
        # Generate a dynamic activation code
        activation_code = generate_activation_code()

        # Send the code via email
        send_activation_email(user.email, activation_code)
