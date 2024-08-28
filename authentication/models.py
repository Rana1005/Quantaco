from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.

class Customer(AbstractUser, PermissionsMixin):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'password']

    def __str__(self):
        return self.phone_number
