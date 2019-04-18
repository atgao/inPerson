from django.shortcuts import render
from django_filters import rest_framework as filters
from django.core import serializers

from . import models
from . import serializers
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.filters import SearchFilter

from .filters import UserFilter


class UserListView(generics.ListCreateAPIView):
    """
    GET user/?search=...
    """
    User = get_user_model()
    queryset = models.User.objects.all();
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_class = UserFilter
    search_fields = ('first_name', 'last_name', 'netid', 'class_year')

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.UserSerializer(queryset, many=True)
<<<<<<< HEAD
        return Response(data=serializer.data, status=status.HTTP_200_OK)
=======
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a new user if one does not exist
    # make sure that user has valid login info
    # def post(self, request):
    #     queryset = models.User.objects.all()
    #     if
>>>>>>> issue-error-codes

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET users/:id/
    """
    User = get_user_model()
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            a_user = self.get_queryset()
            return Response(serializers.UserSerializer(a_user).data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(
                data={"message": "User {} does not exist".format(pk)},
<<<<<<< HEAD
                status=status.HTTP_404_NOT_FOUND)
=======
                status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
>>>>>>> issue-error-codes
