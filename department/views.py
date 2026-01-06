"""
Department Views - Dev A
Nhánh: feature/master-department
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import Department
from .serializers import DepartmentSerializer


class DepartmentListView(generics.ListCreateAPIView):
    """GET/POST: Danh sách & tạo phòng ban"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE: Chi tiết phòng ban"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
