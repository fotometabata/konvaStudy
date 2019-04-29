from rest_framework import viewsets
from django.shortcuts import render
from . import serializers
from .models import Act

# Create your views here.
class ActViewSets(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = serializers.ActSerializer
