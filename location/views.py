"""
Location Views - Dev A
Nhánh: feature/master-location
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import Location
from .serializers import LocationSerializer


class LocationListView(generics.ListCreateAPIView):
    """GET/POST: Danh sách & tạo vị trí"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE: Chi tiết vị trí"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
