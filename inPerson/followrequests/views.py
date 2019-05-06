from django.shortcuts import render
from django.shortcuts import render
from django_filters import rest_framework as filters
from django.db import IntegrityError
from datetime import datetime
import requests

from . models import FollowRequest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

# third-party apps
from friendship.models import Follow, Block
from . serializers import FollowsSerializer, FollowRequestsSerializer, BlocksSerializer

class FollowsListView(generics.ListAPIView):
    """
    GET user/following
    """

    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # return a list of the user's following
    def list(self, request):
        try:
            queryset = Follow.objects.filter(follower=request.user)
            serializer = FollowsSerializer(queryset, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowsDestroyView(generics.DestroyAPIView):
    """
    DELETE unfollow/:userid             unfollow userid
    """

    User = get_user_model()
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # unfollow user with id=pk
    def delete(self, request, pk):
        print(request)
        User = get_user_model()
        followee = User.objects.get(pk=pk)
        try:
            Follow.objects.remove_follower(follower=request.user, followee=followee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        # *** check if correct
        except request.user.DoesNotExist:
            return Response(data={"message": "Cannot unfollow {} since {} not found".format(pk, request.user)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Follow.DoesNotExist:
            return Response(data={"message": "Cannot unfollow {} since {} was not following".format(pk, request.user)},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot unfollow {} since {} not found".format(pk, pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowersListView(generics.ListAPIView):
    """
    GET user/followers
    """

    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # return a list of the user's followers
    def list(self, request):
        try:
            queryset = Follow.objects.filter(followee=request.user)
            serializer = FollowsSerializer(queryset, many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowersRemoveDetailView(generics.DestroyAPIView):
    """
    DELETE remove/:userid                  delete a follower
    """

    User = get_user_model()
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # unfollow user with id=pk
    def delete(self, request, pk):
        User = get_user_model()
        follower = User.objects.get(pk=pk)
        try:
            Follow.objects.remove_follower(follower=follower, followee=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        # *** check if correct
        except request.user.DoesNotExist:
            return Response(data={"message": "Cannot delete follower {} since {} not found".format(pk, request.user)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Follow.DoesNotExist:
            return Response(data={"message": "Cannot delete follower {} since {} was not following".format(pk, pk)},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot delete follower {} since {} not found".format(pk, pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowerRequestsSentListView(generics.ListAPIView):
    """
    GET user/requests/sent
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    def list(self, request):
        try:
            queryset = FollowRequest.objects.filter(from_user=request.user)
            serializer = FollowRequestsSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowerRequestsListView(generics.ListAPIView):
    """
    GET user/requests                   retrieves list of user's follower requests
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    def list(self, request):
        try:
            queryset = FollowRequest.objects.filter(to_user=request.user)
            serializer = FollowRequestsSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowerRequestsCreateView(generics.CreateAPIView):
    """
    POST user/requests/:userid          accepts follow request from userid
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    # pk is the db id from the user to accept the request from
    def post(self, request, pk):
        User = get_user_model()
        from_user = User.objects.get(pk=pk)
        to_user = request.user
        try:
            f_request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            f_request.accept()
            return Response(data={"message": "Follow request from {} accepted by {}".format(pk, request.user)},
                            status=status.HTTP_200_OK)
        # *** check if correct
        except to_user.DoesNotExist:
            return Response(data={"message": "Cannot accept follow request since {} does not exist".format(request.user)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except FollowRequest.DoesNotExist:
            return Response(data={"message": "No follow request from {} to {} exists".format(pk, request.user)},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot accept follow request since {} does not exist".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowerRequestsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT follow/:userid                  request to follow user with userid
    DELETE follow/:userid               delete follow request
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    def put(self, request, pk):
        User = get_user_model()
        follower = request.user
        followee = User.objects.get(pk=pk)
        created = datetime.now()
        if follower == followee:
            return Response(data={"message": "Sent follow request to self"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            # must get message for follow request somehow??
            FollowRequest.objects.create(from_user=follower, to_user=followee,
                                        created=created)
            return Response(data={"message": "{} sent follow request to {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except follower.DoesNotExist:
            return Response(data={"message": "Cannot follow user {} since {} does not exist".format(followee, request.user)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot follow user {} since {} does not exist".format(followee, follower)},
                            status=status.HTTP_404_NOT_FOUND)
        # must test that there is a block or user already follows
        except IntegrityError:
            return Response(data={"message": "Cannot send request to user {} since {} request already exists".format(followee, follower)},
                            status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # pk is of the user to reject the follow request from
    def delete(self, request, pk):
        User = get_user_model()
        follower = User.objects.get(pk=pk)
        try:
            f_request = FollowRequest.objects.get(from_user=follower, to_user=request.user)
            f_request.reject()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except request.user.DoesNotExist:
            return Response(data={"message": "Cannot reject follow request since {} does not exist".format(request.user)},
                    status=status.HTTP_401_UNAUTHORIZED)
        except FollowRequest.DoesNotExist:
            return Response(data={"message": "No follow request from {} to {} exists".format(pk, request.user)},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot reject follow request since {} does not exist".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FollowerRequestsCancelView(generics.CreateAPIView):
    """
    POST cancel/:userid             cancel request to userid
    """

    User = get_user_model()
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestsSerializer

    def post(self, request, pk):
        User = get_user_model()
        from_user = request.user
        to_user = User.objects.get(pk=pk)
        try:
            f_request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            f_request.cancel()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except request.user.DoesNotExist:
            return Response(data={"message": "Cannot cancel follow request to {} since {} does not exist".format(pk, request.user)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except FollowRequest.DoesNotExist:
            return Response(data={"message": "Follow request to {} does not exist".format(pk)},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "Cannot cancel follow request to {} since {} does not exist".format(pk, pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BlocksListView(generics.ListAPIView):
    """
    GET user/blocks/                get list of users that the requesting user is blocking
    """

    queryset = Block.objects.all()
    serializer_class = BlocksSerializer

    def list(self, request):
        try:
            queryset = Block.objects.filter(blocker=request.user)
            serializer = BlocksSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BlocksCreateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    POST blocks/:userid               block user with userid
    GET  blocks/:userid               see if a user is blocking current user
    DELETE blocks/:userid             unblock user with userid
    """

    queryset = Block.objects.all()
    serializer_class = BlocksSerializer

    def post(self, request, pk):
        User = get_user_model()
        blocked = User.objects.get(pk=pk)
        try:
            Block.objects.add_block(request.user, blocked)
            return Response(data={"message": "{} has blocked user {}".format(pk, request.user)},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={"message": "User {} not found".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError: # must be tested
            return Response(data={"message": "Block already exists"},
                            status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, pk):
        User = get_user_model()
        blocker = User.objects.get(pk=pk)
        try:
            Block.objects.is_blocked(blocker, request.user)
            return Response(data={"message": "{} is blocked by {}".format(request.user, pk)},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={"message": "User {} not found".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        User = get_user_model()
        blocked = User.objects.get(pk=pk)
        try:
            Block.objects.remove_block(request.user, blocked)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Block.DoesNotExist:
            return Response(data={"message": "Block does not exist"},
                            status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(data={"message": "User {} not found".format(pk)},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                data={"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
