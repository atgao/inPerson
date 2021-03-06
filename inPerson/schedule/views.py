from django.shortcuts import render
from django_filters import rest_framework as filters
from django.core import serializers

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model

# models and serializers
from .models import Section, RecurrentEvent, Schedule
from .serializers import SectionsSerializer, RecurrentEventsSerializer, SchedulesSerializer
from friendship.models import Follow

# filters
from .filters import SectionFilter

# TODO: THIS STUFF IS ALL FOR RETURN THE CURRENT START/END DATE OF A SEMESTER
from datetime import datetime
import json
import requests

TERM_CODE = 1194  # spring 2019
URL_PREFIX = "http://etcweb.princeton.edu/webfeeds/courseofferings/"
LIST_URL = URL_PREFIX + "?fmt=json&term={term}&subject=all"
DEFAULT_TIME = "00:00"

class RetrieveSemesterDetailView(generics.RetrieveAPIView):
    """
    GET semester            returns start and end date of semester
    """

    def get(self, request):
        try:
            WEBFEED_URL = LIST_URL.format(term=TERM_CODE)
            data = requests.get(WEBFEED_URL).json()['term'][0]
            semester = {"start_date": data["start_date"], "end_date": data["end_date"]}
            return Response(data=semester, status=status.HTTP_200_OK)
        except:
            return Response(data={"message": Error},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    ordering = ('code', 'catalog_number')

    def list(self, request):
        # print("PRINTING REQUEST")
        print(request)
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
    POST user/schedule/classes/
    """
    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

    def post(self, request, *args, **kwargs):
        schedule = Schedule.objects.get_current_schedule_for_user(request.user)
        if schedule.owner != request.user:
            return Response(data={"message": "Not your schedule"},
                            status=status.HTTP_403_FORBIDDEN)
        a_class = request.data["body"]["class"]

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

class ListOtherUserScheduleView(generics.ListAPIView):
    """
    GET schedule/:userid    GETS all recurrent events of a user's current schedule
    """

    queryset = RecurrentEvent.objects.all()
    serializer_class = RecurrentEventsSerializer

    def list(self, request, pk):
        try:
            # get the other user
            User = get_user_model()
            other_user = User.objects.get(pk=pk)

            # get requesting user's following
            if request.user != other_user:
                following = Follow.objects.get(follower=request.user,
                                                 followee=other_user)
            # get the most recent schedule
            schedule = Schedule.objects.get_current_schedule_for_user(other_user)
            events = RecurrentEvent.objects.filter(schedule=schedule)
            serializer = RecurrentEventsSerializer(events, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except Follow.DoesNotExist:
            return Response(data={"message": "Not following user"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateScheduleView(generics.CreateAPIView):
    """
    POST schedule/user         CREATE new schedule
    """

    queryset = Schedule.objects.all()
    serializer_class = SchedulesSerializer

    def post(self, request, *args, **kwargs):
        try:
            s = Schedule.objects.create(request.data, owner=request.user)
            serializer = SchedulesSerializer(s)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteScheduleView(generics.DestroyAPIView):
    """
    DELETE schedule/user
    """
    queryset = Schedule.objects.all()
    serializer_class = SchedulesSerializer

    def delete(self, request, *args, **kwargs):
        try:
            schedule = self.queryset.get(owner=request.user)
            schedule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Schedule.DoesNotExist:
            return Response(data={"message": "Schedule not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={"message": "Error"},
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
        schedule = Schedule.objects.get_current_schedule_for_user(request.user)
        if schedule.owner != request.user:
            return Response(data={"message": "Not your event"},
                            status=status.HTTP_403_FORBIDDEN)
        data = request.data
        try:
            location = ""
            if data.get(location) != None:
                location = data["location"]
            e = RecurrentEvent.objects.create(title=data["title"], start_time=data["start_time"],
                                              end_time=data["end_time"], days=data["days"],
                                              location=data.get(location, ""), schedule=schedule)
            serializer = RecurrentEventsSerializer(e)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        try:
            schedule = Schedule.objects.get_current_schedule_for_user(request.user)
            events = RecurrentEvent.objects.filter(schedule=schedule)
            serializer = RecurrentEventsSerializer(events, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TO DO: MUST VALIDATE THIS DATA
    def put(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            if event.schedule.owner == request.user:
                serializer = RecurrentEventsSerializer()
                updated_event = serializer.update(event, request.data)
                return Response(data=RecurrentEventsSerializer(updated_event).data,
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Not your event"},
                                status=status.HTTP_403_FORBIDDEN)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            event = self.queryset.get(pk=kwargs["pk"])
            if event.schedule.owner == request.user:
                event.delete()
                return Response(data={"message": "Success"},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data={"message": "Not your event"},
                                status=status.HTTP_403_FORBIDDEN)
        except RecurrentEvent.DoesNotExist:
            return Response(data={"message": "Event not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except request.user.DoesNotExist:
            return Response(data={"message": "User does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={"message": "Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
