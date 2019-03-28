from django.shortcuts import render
from rest_framework import generics

from . import models
from . import serializers
from django.contrib.auth import get_user_model

# Create your views here.
class UserListView(generics.ListCreateAPIView):
    queryset = models.User.objects.all();
    serializer_class = serializers.UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET users/:id/
    PUT users/:id/
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            # a_user = self.get_queryset()
            # return Response(UserSerializer(a_user).data)
            return Response(pk)
        except User.DoesNotExist:
            return Response(
                data={"message": "User {} does not exist".format(pk)},
                status=status.HTTP_404_NOT_FOUND
            )
