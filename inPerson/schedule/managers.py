from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

class SectionToEventsManager(models.Manager):
    def create_event_from_section(self, **kwargs):
        title = kwargs["code"] + kwargs["catalog_number"] + kwargs["section"]
        start_time = kwargs["start_time"]
        end_time = kwargs["end_time"]
        days = kwargs["days"]
        location = kwargs["location"]

        event = self.model(title=title, start_time=start_time, end_time=end_time,
                            days=days, location=location)
        event.owner = self.owner
        event.save()
        return event
