"""
Location Views - CRUD Vị trí
============================

Người phụ trách: [Dev A]
Nhánh Git: feature/master-location
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Location
from .serializers import LocationSerializer


class LocationListView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
