from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

# a recurrent event is like a class or precept
# or a scheduled athletic practice
class Classes(models.Model):
    class_number = models.IntegerField()
    code = models.CharField(max_length=10)
    catalog_number = models.CharField(max_length=5)
    title = models.CharField(max_length=200)
    section = models.CharField(max_length=10)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    days = ArrayField(models.CharField(max_length=10,blank=True, null=True))
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{}{} - {}".format(self.code, self.catalog_number, self.section)
