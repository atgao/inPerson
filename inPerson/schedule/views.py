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

class ListRecurrentEventsView(generics.ListCreateAPIView):
    """
    GET recurrevent/user/       GETS all recurrent events of a user
    POST recurrevent/
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer
    # will need to add permissions class in future?? and decorators

    # add validate data
    def post(self, request, schedule, *args, **kwargs):
        # TO DO: must add in check if class!!
        # must also add in error responses
        a_class = args[0]
        e = RecurrentEvent.objects.create_event_from_section(schedule, a_class)
        return Response(data=RecurrentEventsSerializer(e).data,
                        status=status.HTTP_200_OK)

    def list(self, request):
        schedule = Schedule.objects.filter(owner=request.user)
        events = RecurrentEvent.objects.filter(schedule__in=schedule)
        serializer = RecurrentEventsSerializer(events, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

class RecurrentEventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET recurrevent/:id/
    DELETE recurrevent/:id/
    PUT recurrevent/:id/        UPDATES recurring event

    TO DO: (would this be here??)
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

    # TO DO: MUST VALIDATE THIS DATA
    def put(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            serializer = RecurrentEventsSerializer()
            updated_event = serializer.update(event, request.data)
            return Response(data=RecurrentEventsSerializer(updated_event).data,
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            event = self.querset.get(pk=kwargs["pk"])
            event.delete()
            return Response(data={"message": "Event successfully deleted"},
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
