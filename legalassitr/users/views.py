
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, ForgotPasswordSerializer, PasswordResetSerializer

class LoginView(APIView):
    """ This view povides the Login API functionality """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
            

class LogoutView(APIView):
    """ This view provides the User Logout functionality"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            refresh_token = data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token or token has already been used"}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    """ Provides functionality of Token Refresh """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"detail": "Invalid token or token has expired"}, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    """ This APIView provides functionality for user registration """

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer.create(data=request.data)
        if serializer.is_valid():
            
            # Generate and Send OTPs for email and phone verification
            email_otp = generate_otp()
            phone_otp = generate_otp()

            send_otp_to_email(serializer.validated_data['email'], email_otp)
            send_otp_to_phone(serializer.validated_data['phone_number'], phone_otp)

            # Save the user with unverified email and phone
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(APIView):
    """This provided API for user details and update"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(request):
        # Update the details of the authenticated user
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ForgotPasswordView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

            # send email with password reset url
            # TODO : Design a nice looking email template
            subject = 'Password Reset'
            body = f'Click the following link to reset your password: {reset_url}'
            to_email = [email]
            email_message = EmailMessage(subject, body, to=to_email)
            email_message.send()

            return Response({'detail': 'Password reset mail sent'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetView(APIView):
    def post(self, request, uid_b64, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_text(urlsafe_base64_decode(uid_b64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                password = serializer.validated_data.get('password', None)
                user.set_password(password)
                user.save()

                return Response({'detail': 'Password reset successfully'})
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

