from django.shortcuts import render
from rest_framework import generics
from .models import Section
from .serializers import SectionsSerializer


class ListSectionsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer
