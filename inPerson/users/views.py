from django.shortcuts import render
from django_filters import rest_framework as filters
from django.core import serializers

from . import models
from . import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth import get_user_model

# third-party apps
from friendship.models import Friend, Follow, Block
from .serializers import FriendsSerializer, FollowsSerializer

class UserListView(generics.ListCreateAPIView):
    User = get_user_model()
    queryset = models.User.objects.all();
    serializer_class = serializers.UserSerializer

    def list(self, request):
        queryset = models.User.objects.all(); #why does this have to be here
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    # create a new user if one does not exist
    # make sure that user has valid login info
    # def post(self, request):
    #     queryset = models.User.objects.all()
    #     if

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
            return Response(serializers.UserSerializer(a_user).data)
            # return Response(pk)
        except models.User.DoesNotExist:
            return Response(
                data={"message": "User {} does not exist".format(pk)},
                status=status.HTTP_404_NOT_FOUND
            )

class FollowsListView(generics.ListCreateAPIView):
    """
    GET users/following
    """

    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # return a list of the user's friends
    def list(self, request):
        queryset = Follow.objects.following(request.user)
        serializer = FollowsSerializer(queryset, many=True)
        # print(serializer.data)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    # TODO : add validate data
    # def post(self, request, to_user):
    #     other_user = User.objects.get(pk=)


class FriendsListView(generics.ListCreateAPIView):
    """
    GET users/following
    """

    queryset = Friend.objects.all()
    serializer_class = FriendsSerializer

    # return a list of the user's friends
    def list(self, request):
        queryset = Friend.objects.friends(request.user)
        serializer = FriendsSerializer(queryset, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    # TODO : add validate data
    # def post(self, request, to_user):
    #     other_user = User.objects.get(pk=)
