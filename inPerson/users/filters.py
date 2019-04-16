from .models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "netid", "class_year"]
