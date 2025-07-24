from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    diponame = models.CharField(max_length=500,null=True)
    role = models.CharField(max_length=500,null=True)