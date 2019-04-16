from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from . managers import CustomUserManager

class User(AbstractUser):
    netid = models.CharField(max_length=15, unique=True, default="", null=False)
    class_year = models.IntegerField(blank=False, default=2022)
    email = models.CharField(max_length=15, default=None, null=True)
    university = models.CharField(max_length=20, default="", null=False)


    #USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'class_year', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.username)

    def get_name(self):
        return "{} {}".format(self.first_name, self.last_name)
