from django.db import models
from datetime import time
from django.contrib.postgres.fields import ArrayField

class SectionToEventsManager(models.Manager):
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
