
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework import serializers

from .email_utils.email import send_forgot_password_email
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'email', 'email_verifier', 'phone_verifier')
        extra_kwargs = {'email': {'read_only': True}}

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number')
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.get('password', None)
        instance = self.Meta.model.create_user(**validated_data) #doesnt include password

        if password is not None:
            instance.set_password(password) #hashes password
        instance.save()
        return instance
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator()
        user.save()

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}&email={email}"
        send_forgot_password_email(email, reset_link=reset_link)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if not default_token_generator.check_token(user, attrs['token']):
                raise serializers.ValidationError('Invalid token')
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return attrs
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()

