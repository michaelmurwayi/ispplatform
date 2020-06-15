# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class Packages(models.Model):
    bundle = models.CharField(max_length=20)
    bundle_price = models.IntegerField()
    bundle_length = models.CharField(max_length=10)
    bundle_speed = models.CharField(max_length=15)


class CustomUser(AbstractBaseUser):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    phonenumber = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phonenumber']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class SelectedPackages(models.Model):
    email = models.CharField(max_length=64)
    bundle = models.CharField(max_length=10)
    speed = models.CharField(max_length=10)
    Expiry = models.CharField(max_length=50)
    balance = models.CharField(max_length=100)
    access_period = models.CharField(max_length=10)
