from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        OFFICE = "OFFICE", 'Escritório'
        TECHNICIAN = "TECHNICIAN", 'Técnico'

    role = models.CharField(max_length=100, choices=Role.choices)
    phone_number = models.CharField(max_length=20, blank=True)
