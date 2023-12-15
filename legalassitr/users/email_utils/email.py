from enum import Enum

from django.core.mail import send_mail
from django.template.loader import render_to_string

SENDER_EMAIL = "support@legalassistr.com"


class EmailType(Enum):
    ORDER_EMAIL = 'order'
    LOGIN_MAIL = 'login'
    DELIVERY_NEAR = 'delivery'
    DELIVERED = 'delivered'
    FEEDBACK = 'feedback'


def send_login_alert_email(user_email, device_name, location, date_time):
    subject = 'Legal Assistr - Login Alert : Suspicious Activity Detected'
    html_message = render_to_string('./templates/login_alert.html',{
        'user': user_email,
        'device_name': device_name,
        'location': location,
        'date_time': date_time,
    })
    
    send_mail(subject, f'Login Alert, your account was recently logged in on {device_name} from {location} at {date_time}. Please make sure this was you.', SENDER_EMAIL, [user_email], html_message=html_message)


def send_order_confirmation_email(customer_name, customer_email, order_details):
    subject = f'Legal Assitr - Order Confirmation : Your order has been placed.'
    html_message = render_to_string('./templates/order_confirm.html', {
        "customer": customer_name,
        'order_details': order_details
    })

    send_mail(subject, 'Your order has been placed. Please check the app for more details.', SENDER_EMAIL, [customer_email], html_message=html_message)