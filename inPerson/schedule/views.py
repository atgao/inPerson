from django.shortcuts import render
from django_filters import rest_framework as filters
from django.core import serializers

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.filters import SearchFilter

from .models import Section, RecurrentEvent, Schedule
from .serializers import SectionsSerializer, RecurrentEventsSerializer, SchedulesSerializer

from .filters import SectionFilter

class ListSectionsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_class = SectionFilter
    search_fields = ('code', 'catalog_number', 'title', 'term')
    #
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SectionsSerializer(queryset, many=True)
        return Response(serializer.data)

class ListRecurrentEventsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

class RecurrentEventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET recurrevent/:id/
    POST recurrevent/           CREATES PERSONAL recurring event
    DELETE recurrevent/:id/
    PUT recurrevent/:id/        UPDATES recurring event

    TO DO:
    POST recurrevent/:groupid   CREATES GROUP recurring event
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

    def get(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            return Response(RecurrentEventsSerializer(event).data)
        except RecurrentEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ListSchedulesView(generics.ListAPIView):
    """
    Lists all schedules of all users.
    """
    queryset = Schedule.objects.all()
    serializer_class = SchedulesSerializer
