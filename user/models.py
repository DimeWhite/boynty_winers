from django.db import models
from django.contrib.auth.models import AbstractUser
from lot.models import Lot


class User(AbstractUser):
    middle_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(unique=True, blank=False)
    balance = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

