from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class Role(Enum):
    INACTIVE = 1
    EMPLOYEE = 2
    MANAGER = 3
    ADMIN = 4

    @classmethod
    def choices(cls):
        return [(role.value, role.name.replace('_', ' ').capitalize()) for role in cls]


class Position(models.Model):
    ROLE_CHOICES = Role.choices()

    title = models.CharField(max_length=100, unique=True)
    rights_level = models.IntegerField(choices=ROLE_CHOICES)


    def __str__(self):
        return self.title


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_terminated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"