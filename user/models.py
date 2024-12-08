from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password and role
        """
        extra_fields.setdefault("role", "Admin")

        # Ensure the password and email are provided
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    email = models.EmailField(unique=True)  # Make email unique for each user.
    username = models.CharField(max_length=150, blank=True, null=True)  # Optional username field

    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = []  # Remove username as a required field

    objects = CustomUserManager()  # Link to the custom user manager

    def __str__(self):
        return self.email
