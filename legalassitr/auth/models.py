# Import necessary modules from Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Define a Manager class for handling user creation and management
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Method to create a user

        Args:
        - email : The email of the user
        - password : The password of the user
        - **extra_fields : The other fields like first_name, last_name, etc

        Returns:
        - `User` instance of the created user
        """
        if not email:
            raise ValueError('The email field must be set')
        # normalize the email (make it lowercase) for consistency
        email = self.normalize_email(email)
        # create the new user instance with the provided email
        user = self.model(email=email, **extra_fields)
        # set the user password's hash in a secure manner
        user.set_password(password)
        # save the user in the database
        user.save(using=self._db)
        # return the created user
        return user

    def create_staff(self, email, password=None, **extra_fields):
        """
        Method to create a staff user
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    def create_expert(self, email, password=None, **extra_fields):
        """
        Method to create an expert user
        """
        extra_fields.setdefault('is_expert', True)
        return self.create_user(email, password, **extra_fields)
    
        
    
# we define a custom user model that will store the extra data we need
# for the app
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    # sets if the user is admin staff
    is_staff = models.BooleanField(default=False)
    # sets if the user is expert
    is_expert = models.BooleanField(default=False)

    # use the user manager for managing user objects
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email