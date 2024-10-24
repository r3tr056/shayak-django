import requests

from django.utils import timezone
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import (
    LoginAttempt,
    User
)
from users.utils import (
    send_otp_to_phone,
    verify_phone_otp
)
from users.email_utils.email import (
    send_otp_to_email,
    verify_email_otp,
    send_login_alert_email
)
from users.serializers import (
    UserRegistrationSerializer,
    ForgotPasswordSerializer,
    UserProfileSerializer,
    PasswordResetSerializer,
)

class LoginView(APIView):
    """ This view povides the Login API functionality """

    def authenticate_user(self, email, password):
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
    def get_location(self, request):
        ip = request.META.get('REMOTE_ADDR')
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                return response.json().get('country', 'Unknown')
        except requests.RequestException:
            pass
        return 'Unknown'
    
    def is_unusual_login(self, user, location, device_id):
        last_login_attempt = LoginAttempt.objects.filter(user=user).last()
        if last_login_attempt:
            return (last_login_attempt.location != location or last_login_attempt.device != device_id)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_agent = request.META.get('HTTP_USER_AGENT')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.authenticate_user(email, password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        
        location = self.get_location(request)
        device_id = user_agent

        LoginAttempt.objects.create(
            user=user,
            location=location,
            device_id=device_id,
            timestamp=timezone.now()
        )

        if self.is_unusual_login(user, location, device_id):
            # Send a login email async
            send_login_alert_email.delay(user.email, user.username, location, device_id)

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        response_data = {
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
            'email': user.email,
            'user_type': user.user_type,
        }

        response = Response(data=response_data, status=status.HTTP_200_OK)

        response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True)  #httonly - frontend can't access cookie, only for backend
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token is None:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK).delete_cookie('refresh_token')
        except TokenError:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserRegisterationView(generics.CreateAPIView):
    """ This APIView provides functionality for user registration """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_verification_email(user)
        self.send_verification_sms(user)
        return Response({"message": "Sent OPT to email and phone number"}, status=status.HTTP_200_OK)

    def send_verification_email(self, user):
        send_otp_to_email(user.email)

    def send_verification_sms(self, user):
        send_otp_to_phone(user.phone_number)
    
class VerifyOTPView(APIView):
    def get(self, request, *args, **kwargs):
        """ Re-Request otp """
        email = request.data.get('email')
        phone = request.data.get('phone')
        if not email or phone:
            return Response({'error': 'Email or phone is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            send_otp_to_email(email)
            return Response({'message': f'OTP sent to {email}'}, status=status.HTTP_200_OK)
        if phone:
            send_otp_to_phone(phone)
            return Response({'message': f'OTP sent to {phone}'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Unable to process OTP request.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """ Send either of the OTP along with the credential """

        email = request.data.get('email')
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        if not otp:
            return Response({'error': 'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            if not User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            if verify_email_otp(email, otp):
                user = User.objects.get(email=email)
                user.email_verified = True
                user.save()
                return Response({'message': 'Email OTP verification successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP for email.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if phone:
            if not User.objects.filter(phone=phone).exists():
                return Response({'error': 'User with this phone does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            if verify_phone_otp(phone, otp):
                user = User.objects.get(phone=phone)
                user.phone_verified = True
                user.save()
                return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP for phone.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Either email or phone along with OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)

    
class UserView(generics.RetrieveUpdateAPIView):
    """This provided API for user details and update"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user
    
class ForgotPasswordView(generics.GenericAPIView):
    """ API View for initiating a password reset process by sending a reset link via email. """
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    

