from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

# each class is a class on the princeton course registrar website
# i.e., COS126 L01 and COS126 P01 would be considered different classes
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

# a recurrent event is an event that occurs on a regular basis at the same
# time every week, such as a sports practice or class. note that classes are
# TRANFORMED into a recurrent event
class RecurrentEvent(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    days = ArrayField(models.CharField(max_length=10,blank=False, null=False))
    location = models.CharField(max_length=200, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {}-{}".format(self.title, self.location, self.start_time, self.end_time)

class Schedule(models.Model):
    semester = models.CharField(max_length=5, blank=False, null=False) #F18, S19, etc
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.semester)
