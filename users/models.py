from django.db import models
from django.contrib.auth.models import AbstractUser
from users.apps import GENDER_CHOICES

class CustomUser(AbstractUser):    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    name = models.CharField(max_length=150)
