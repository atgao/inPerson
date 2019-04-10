from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from schedules.models import Schedule

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager.
    """
    def create_user(self, first_name, last_name, username, class_year, password, email=None):
        """
        Create and save a User with the given email and password.
        """
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, username, class_year, password, email=None):
        """
        Create and save a SuperUser with the given password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(first_name, last_name, username, class_year, password, email=None)

    def get_current_schedule(self, first_name, last_name, username):
        user = User.objects.get(first_name=first_name, last_name=last_name, username=username)
        schedules = Schedule.objects.filter(owner=user)
        
