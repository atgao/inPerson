from rest_framework import serializers
from .models import Section, RecurrentEvent, Schedule

class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("code", "catalog_number", "section", "title",
                  "start_time", "end_time", "days", "location")

class RecurrentEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrentEvent
        fields = ("title", "start_time", "end_time", "days", "location")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.days = validated_data.get("days", instance.days)
        instance.location = validated_data.get("title", instance.location)

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("semester", "owner")
