
import jwt
from twilio.rest import Client
from django.conf import settings

from functools import wraps
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from users.models import User

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
verify_sid = settings.TWILIO_VERIFY_SID

twilio_client = Client(account_sid, auth_token)

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('jwt_token')
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")

        user_id = payload.get('user_id')
        if user_id is None:
            raise AuthenticationFailed("Invalid token payload.")
        
        user = User.objects.filter(id=user_id).first()

        if not user:
            raise AuthenticationFailed("User not found.")
        
        return (user, None)
    
    def authenticate_header(self, request):
        return 'JWT'


def expert_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated and user.is_expert:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
    return _wrapped_view

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated and user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
    return _wrapped_view


def send_otp_to_phone(phone_number):
    verification = twilio_client.verify.v2.services(verify_sid).verifications.create(to=phone_number, channel="sms")
    return verification.status

def verify_phone_otp(phone_number, otp):
    verification_check = twilio_client.verify.v2.services(verify_sid).verification_checks.create(to=phone_number, code=otp)
    if verification_check.status == 'approved':
        User.objects.verify_user(phone_number=phone_number)
    return verification_check.status

