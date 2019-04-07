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
from .serializers import FollowsSerializer

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

    # return a list of the user's following
    def list(self, request):
        # queryset = Follow.objects.following(request.user)
        queryset = Follow.objects.filter(follower=request.user)
        serializer = FollowsSerializer(queryset, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    # TODO : add validate data
    # def post(self, request, to_user):
    #     other_user = User.objects.get(pk=)

class FollowersListView(generics.ListCreateAPIView):
    """
    GET users/followers
    """

    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # return a list of the user's followers
    def list(self, request):
        # queryset = Follow.objects.following(request.user)
        queryset = Follow.objects.filter(followee=request.user)
        serializer = FollowsSerializer(queryset, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

class FollowersRelationshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT follow/:userid                  request to follow user with userid
    DELETE follow/:userid/reject        delete follow request
    """

    User = get_user_model()
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # TO DO: MUST VALIDATE THIS DATA
    # LOGIN IS REQUIRED
    def put(self, request, pk):
        follower = request.user
        followee = models.User.objects.get(pk=pk)
        try:
            Follow.objects.add_follower(follower, followee)
            return Repsonse(data={"{} sent follow request to {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(data={"Cannot follow user {} since {} does not exist".format(pk, pk)},
                            status=status.HTTP_404_NOT_FOUND)

    # LOGIN IS REQUIRED
    # pk is of the user to be ignored
    def delete(self, request, pk):
        follower = request.user
        followee = models.User.objects.get(pk=pk)
        try:
            Follow.objects.remove_follower(follower, followee)
            return Response(data={"{} rejected follow request from {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
