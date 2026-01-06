"""
Person Views - Dev A
Nhánh: feature/master-person
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import Person
from .serializers import PersonSerializer


class PersonListView(generics.ListCreateAPIView):
    """
    GET/POST: Danh sách & tạo cá nhân
    Query params: department=<id>
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Filter by department


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE: Chi tiết cá nhân"""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
