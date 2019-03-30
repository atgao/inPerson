from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.core import serializers

from .models import Section
from .serializers import SectionsSerializer


class ListSectionsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer

class SectionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Examine individual details of a class
    """
    queryset = Section.objects.all()
    serializer_class = SectionsSerializer

    def get(self, request, *args, **kwargs):
        a_section = Section.objects.get(pk=kwargs['pk'])
        return Response(SectionsSerializer(a_section).data)
    #
    # def get_queryset(self):
    #     class_number = self.kwargs['code']
    #     queryset = self.queryset.filter(code=code)
    #     return queryset
