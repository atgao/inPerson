from django.shortcuts import render
from rest_framework import generics
from .models import Classes
from .serializers import ClassesSerializer


class ListClassesView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
