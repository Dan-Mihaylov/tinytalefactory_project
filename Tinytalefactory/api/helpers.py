from django.core.mail import send_mail
from smtplib import SMTPException
import os

def create_email_message(email: str, question: str) -> str:
    return f'Message from:\n{email}\n\nMessage:\n{question}'


def send_email(email: str, question: str) -> bool:
    message = create_email_message(email, question)
    try:
        send_mail(
            subject='Tiny Tale Factory Contact Us Form Submission',
            message=message,
            recipient_list=[os.getenv('MY_EMAIL')],
            from_email=os.getenv('DEFAULT_EMAIL'),
        )
        return True
    except SMTPException as e:
        return False
