
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from auth.models import User
from auth.serializers import UserSerializer, LoginSerializer, ForgotPasswordSerializer, PasswordResetSerializer

RESET_FORMAT_URL = 'https://your-reset-url.com/reset/{uid}/{token}/'

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(request):
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
        return Response(serializer.data)
    
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

            reset_url = RESET_FORMAT_URL.format(uid=uid, token=token)

            # send email with password reset url
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
    
