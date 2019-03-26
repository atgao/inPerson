from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    #netid = models.CharField(max_length=15, unique=True, default=None, null=True)
    class_year = models.IntegerField(blank=False, default=2022)
    email = models.CharField(max_length=15, default=None, null=True)

    #
    REQUIRED_FIELDS = ['first_name', 'last_name', 'class_year', 'email']

    def __str__(self):
        return "{}".format(self.username)
