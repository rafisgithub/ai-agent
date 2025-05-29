from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from datetime import timedelta
import datetime

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class OTP(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length = 6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expire = self.created_at + timedelta(minutes=5)
        if expire < datetime.now():
            return True
        return False