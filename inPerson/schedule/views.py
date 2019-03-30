from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.core import serializers

from .models import Section
from .models import RecurrentEvent
from .models import Schedule
from .serializers import SectionsSerializer
from .serializers import RecurrentEventsSerializer
from .serializers import SchedulesSerializer


class ListSectionsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer

class SectionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Examine individual details of a class
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer

    def get(self, request, *args, **kwargs):
        a_section = Section.objects.get(pk=kwargs['pk'])
        return Response(SectionsSerializer(a_section).data)
    #
    # def get_queryset(self):
    #     class_number = self.kwargs['code']
    #     queryset = self.queryset.filter(code=code)
    #     return queryset

class ListRecurrentEventsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

class ListSchedulesView(generics.ListAPIView):
    """
    Lists all schedules of all users.
    """
    queryset = Schedule.objects.all()
    serializer_class = SchedulesSerializer
