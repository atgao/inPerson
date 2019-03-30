from rest_framework import serializers
from .models import Section

class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("code", "catalog_number", "section", "title",
                  "start_time", "end_time", "days", "location")
