# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Messages(models.Model):
<<<<<<< HEAD

    message = models.TextField(max_length=100)


class UseraccessSelectedpackages(models.Model):
    bundle = models.CharField(max_length=10)
    speed = models.CharField(max_length=10)
    expiry = models.CharField(db_column='Expiry', max_length=50)  # Field name made lowercase.
    balance = models.CharField(max_length=100)
    access_period = models.CharField(max_length=10)
    username = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'useraccess_selectedpackages'
=======
    message = models.TextField(max_length=100)
>>>>>>> af412d69c1319e7d0403c408175145c5bc607b8a
