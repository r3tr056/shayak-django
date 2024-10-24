
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, user_type='normal', **extra_fields):
        """
        Method to create a user
        """
        if not email:
            raise ValueError('The email field must be set')
        if user_type not in ['normal', 'expert', 'admin']:
            raise ValueError('Invalid user type')
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def verify_user(self, email, phone):
        user = self.model(email=email) or self.model(phone=phone)
        user.verified = True
        user.save()

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Method to create a superuser user
        """
        if not email:
            raise ValueError("The email field must be set")
        
        email = self.normalize_email(email)
        return self.create_user(email, password, user_type='admin', **extra_fields)
    
    def create_expert(self, email, password=None, **extra_fields):
        """
        Method to create an expert user
        """
        return self.create_user(email, password, user_type='expert', **extra_fields)
    
    def delete_user(self, email):
        user = self.model(email=email)
        user.is_active = False
        user.save(user=self._db)

class LoginAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.email} - {self.timestamp} - {self.location} - {self.device_id}"

class User(AbstractBaseUser):
    USER_TYPES = (
        ('normal', 'Normal User'),
        ('expert', 'Expert User'),
        ('admin', 'Admin User'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True)
    phone_number = PhoneField(blank=True, help_text='User phone number')
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')
    
    # store the user location field
    location = models.CharField(max_length=255, null=True, blank=True)
    last_login_attempt = models.ForeignKey(LoginAttempt, on_delete=models.CASCADE, related_name='login_attemp')

    # use the user manager for managing user objects
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email','first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email
    
class Feature(models.Model):
    name = models.CharField(max_length=255)
    
class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    ai_creativity_level = models.IntegerField()
    allowed_features = models.ManyToManyField(Feature, blank=True)
