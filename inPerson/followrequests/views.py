from django.shortcuts import render
from django.shortcuts import render
from django_filters import rest_framework as filters
from datetime import datetime

from . models import FollowRequest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth import get_user_model

# third-party apps
from friendship.models import Follow, Block
from . serializers import FollowsSerializer, FollowRequestsSerializer

class FollowsListView(generics.ListAPIView):
    """
    GET user/following
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

class FollowsDestroyView(generics.DestroyAPIView):
    """
    DELETE unfollow/:userid             unfollow userid
    """

    User = get_user_model()
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # unfollow user with id=pk
    def delete(self, request, pk):
        followee = models.User.get(pk=pk)
        try:
            follow = Follow.objects.filter(follower=request.user, followee=followee)
            return Response(data={"{} unfollowed {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(data={"Cannot unfollow {}".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)

class FollowersListView(generics.ListAPIView):
    """
    GET user/followers
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

class FollowersRemoveDetailView(generics.DestroyAPIView):
    """
    DELETE remove/:userid                  delete a follower
    """

    User = get_user_model()
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # unfollow user with id=pk
    def delete(self, request, pk):
        follower = models.User.get(pk=pk)
        try:
            follow = Follow.objects.filter(follower=follower, followee=request.user)
            return Response(data={"{} unfollowed {}".format(pk, request.user)},
                            status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(data={"Cannot unfollow {}".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)


class FollowerRequestsListCreateView(generics.ListCreateAPIView):
    """
    GET user/requests                   retrieves list of user's follower requests
    POST user/requests/:userid          accepts follow request from userid
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer
    # TODO: LOGIN IS REQUIRED
    # pk is the db id from the user to accept the request from
    def post(self, request, pk):
        from_user = models.User.objects.get(pk=pk)
        to_user = request.user
        try:
            request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            request.accept()
            return Response(data={"Follow request from {} accepted by {}".format(pk, request.user)},
                            status=status.HTTP_200_OK)
        except FollowRequest.DoesNotExist:
            return Response(data={"No follow request between {} to {} exists".format(pk, request.user)},
                            status=status.HTTP_200_OK)

    # TODO : LOGIN IS REQUIRED
    def list(self, request):
        queryset = FollowRequest.objects.filter(to_user=request.user)
        serializer = FollowRequestsSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class FollowerRequestsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT follow/:userid                  request to follow user with userid
    DELETE follow/:userid               delete follow request
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    # TO DO: MUST VALIDATE THIS DATA
    # LOGIN IS REQUIRED
    def put(self, request, pk):
        follower = request.user
        followee = models.User.objects.get(pk=pk)
        created = datetime.datetime.now()
        try:
            # must get message for follow request somehow??
            FollowRequest.objects.create(from_user=follower, to_user=followee,
                                        created=created)
            return Repsonse(data={"{} sent follow request to {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(data={"Cannot follow user {} since {} does not exist".format(pk, pk)},
                            status=status.HTTP_404_NOT_FOUND)

    # LOGIN IS REQUIRED
    # pk is of the user to reject the follow request from
    def delete(self, request, pk):
        follower = request.user
        followee = models.User.objects.get(pk=pk)
        try:
            request = FollowRequest.objects.get(from_user=follower, to_user=followee)
            request.reject()
            return Response(data={"{} rejected follow request from {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except FollowRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FollowerRequestsCancelView(generics.CreateAPIView):
    """
    POST cancel/:userid             cancel request from userid
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    def post(self, request, pk):
        from_user = models.User.objects.get(pk=pk)
        to_user = request.user
        try:
            request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            request.cancel()
            return Reponse(data={"Canceled follow request from {}".format(pk)},
                           status=status.HTTP_200_OK)
        except FollowRequest.DoesNotExist:
            return Response(data={"Follow Request does not exist from {}".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
