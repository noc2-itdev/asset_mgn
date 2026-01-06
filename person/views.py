"""
Person Views - CRUD Cá nhân
===========================

Người phụ trách: [Dev A]
Nhánh Git: feature/master-person
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Person
from .serializers import PersonSerializer


class PersonListView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset.select_related('department')


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
