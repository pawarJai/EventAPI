from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def __str__(self):
        return self.email
