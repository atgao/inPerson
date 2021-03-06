from django.db import models
from datetime import time
from django.contrib.postgres.fields import ArrayField

# from .models import Schedule
from users.models import User
from django.contrib.auth import get_user_model

class RecurrentEventsManager(models.Manager):
    # make sure the sections model is serialized then comes in as a dictionary
    def create_event_from_section(self, schedule, *args, **kwargs):
        dict = args[0]
        title = "{}{} {}: {}".format(dict["code"], dict["catalog_number"],
                dict["section"], dict["title"])
        start_time = dict["start_time"]
        end_time = dict["end_time"]
        days = dict["days"]
        location = dict["location"]

        event = self.model(title=title, start_time=start_time, end_time=end_time,
                            days=days, location=location, schedule=schedule)
        event.save()
        return event

    def add_event_to_schedule(self, schedule, *args, **kwargs):
        event = self.create(schedule=schedule, title=args["title"],
                            start_time=args["start_time"], end_time=args["end_time"],
                            days=args["days"], location=args["location"])
        return event

class CurrentScheduleManager(models.Manager):
    def get_current_schedule_for_user(self, user, *args, **kwargs):
        schedules = self.filter(owner=user)
        if schedules.count() == 0:
            return
        current_schedule = schedules[0]
        current_term = current_schedule.term
        for schedule in schedules: # find the most recent schedule
            term = schedule.term
            if int(term[-4:]) > int(current_term[-4:]):
                current_schedule = schedule
                break
            # python compares strings by ASCII vals
            # S has larger ASCII val than F
            elif int(term[-4:]) == int(current_term[-4:]):
                if term[0] < current_term[0]:
                    current_schedule = schedule
                    break
        return current_schedule
