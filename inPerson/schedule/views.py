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
    GET classes/?search=....
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
        try:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except request.user.DoesNotExist:
            return Response(data={"message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"message": Error},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateSectionstoScheduleView(generics.ListCreateAPIView):
    """
    POST classes/
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

    def post(self, request, *args, **kwargs):
        schedule = Schedule.objects.get_current_schedule_for_user(request.user)
        a_class = request.data
        if a_class["term"] != schedule.term: # can't add section when its not same term
            return Response(data={"message": "Class is not in same term"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            e = RecurrentEvent.objects.create_event_from_section(schedule, a_class)
            return Response(data=RecurrentEventsSerializer(e).data,
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except request.user.DoesNotExist:
            return Response(data={"message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"message": Error},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCreateRecurrentEventsView(generics.ListCreateAPIView):
    """
    GET  events/user/       GETS all recurrent events of a user
    POST events/user/       CREATE custom recurrent event
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer
    # will need to add permissions class in future?? and decorators

    # add validate data
    def post(self, request, *args, **kwargs):
        # TO DO: must add in check if class!!
        # must also add in error responses
        schedule = Schedule.objects.get_current_schedule_for_user(request.user)
        try:
            e = RecurrentEvent.objects.create(request.data, schedule=schedule)
            return Response(data={"Created event {}".format(e.pk)},
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Could not create event"},
                            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        schedule = Schedule.objects.get_current_schedule_for_user(request.user)
        events = RecurrentEvent.objects.filter(schedule=schedule)
        serializer = RecurrentEventsSerializer(events, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

class RecurrentEventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET events/:id/
    DELETE events/:id/
    PUT events/:id/        UPDATES recurring event
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

    def get(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            return Response(data=RecurrentEventsSerializer(event).data,
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
            event = self.queryset.get(pk=kwargs["pk"])
            event.delete()
            return Response(data={"message": "Event successfully deleted"},
                            status=status.HTTP_200_OK)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
