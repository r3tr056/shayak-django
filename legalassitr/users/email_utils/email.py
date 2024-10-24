from enum import Enum
import pyotp

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.cache import cache
from django.template.loader import render_to_string


SENDER_EMAIL = settings.SERVER_EMAIL
OTP_EXPIRATION_TIME = 900 # 15 mins

def get_email_otp_cache_key(email):
    return f'opt_email_{email}'

class EmailType(Enum):
    ORDER_EMAIL = 'order'
    LOGIN_MAIL = 'login'
    DELIVERY_NEAR = 'delivery'
    DELIVERED = 'delivered'
    FEEDBACK = 'feedback'

@shared_task
def send_forgot_password_email(user_email, reset_link):
    subject = 'Password Reset'
    body = f'Click the following link to reset your password: {reset_link}'
    to_email = [user_email]
    send_mail(subject, body, SENDER_EMAIL, to_email)

@shared_task
def send_login_alert_email(user_email, device_name, location, date_time):
    subject = 'Legal Assistr - Login Alert : Suspicious Activity Detected'
    html_message = render_to_string('./templates/login_alert.html',{
        'user': user_email,
        'device_name': device_name,
        'location': location,
        'date_time': date_time,
    })
    
    send_mail(subject, f'Login Alert, your account was recently logged in on {device_name} from {location} at {date_time}. Please make sure this was you.', SENDER_EMAIL, [user_email], html_message=html_message)

@shared_task
def send_order_confirmation_email(customer_name, customer_email, order_details):
    subject = f'Legal Assitr - Order Confirmation : Your order has been placed.'
    html_message = render_to_string('./templates/order_confirm.html', {
        "customer": customer_name,
        'order_details': order_details
    })

    send_mail(subject, 'Your order has been placed. Please check the app for more details.', SENDER_EMAIL, [customer_email], html_message=html_message)
    

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.now()


def send_otp_to_email(customer_email):
    otp = generate_otp()
    cache_key = get_email_otp_cache_key(customer_email)
    cache.set(cache_key, otp, timeout=OTP_EXPIRATION_TIME)
    subject = f'Legal Assistr - OTP For Login'
    html_message = render_to_string('emails/otp.html', {
        "otp": otp
    })
    send_mail(subject, f'The OTP for Login is - {otp}', SENDER_EMAIL, [customer_email], html_message=html_message)

def verify_email_otp(customer_email, otp):
    cache_key = get_email_otp_cache_key(customer_email)
    stored_otp = cache.get(cache_key)
    cache.delete(cache_key)
    return otp == stored_otp
