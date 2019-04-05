from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

from .managers import SectionToEventsManager

class Schedule(models.Model):
    term = models.CharField(max_length=5, blank=False, null=False) #F2018, S2019, etc
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="student", related_query_name="students")

    class Meta:
        ordering = ['owner']

    def __str__(self):
        return "{} {}".format(self.owner.username, self.term)

# a section is a section of a class i.e., COS126 L01 and COS126 P01
# would be considered different sections
class Section(models.Model):
    term = models.CharField(max_length=5)
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
    title = models.CharField(max_length=200, blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    days = ArrayField(models.CharField(max_length=10,blank=False, null=False))
    location = models.CharField(max_length=200, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    objects = SectionToEventsManager()

    class Meta:
        ordering = ['schedule', 'start_time']

    def __str__(self):
        return "{} {} {}-{}".format(self.title, self.location, self.start_time, self.end_time)
