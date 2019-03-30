from rest_framework import serializers
from .models import Section
from .models import RecurrentEvent
from .models import Schedule

class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("code", "catalog_number", "section", "title",
                  "start_time", "end_time", "days", "location")

class RecurrentEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrentEvent
        fields = ("title", "start_time", "end_time", "days", "location")

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("semester", "owner")
