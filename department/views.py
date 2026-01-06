"""
Department Views - CRUD Phòng ban
=================================

Người phụ trách: [Dev A]
Nhánh Git: feature/master-department

API Endpoints:
- GET    /api/departments/      → DepartmentListView
- POST   /api/departments/      → DepartmentListView
- GET    /api/departments/<id>/ → DepartmentDetailView
- PUT    /api/departments/<id>/ → DepartmentDetailView
- DELETE /api/departments/<id>/ → DepartmentDetailView
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Department
from .serializers import DepartmentSerializer


class DepartmentListView(generics.ListCreateAPIView):
    """
    GET: Danh sách phòng ban
    POST: Tạo phòng ban mới
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Chi tiết phòng ban
    PUT: Cập nhật phòng ban
    DELETE: Xóa phòng ban
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
