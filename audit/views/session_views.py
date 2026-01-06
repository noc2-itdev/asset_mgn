"""
AuditSession Views - Quản lý đợt kiểm kê
=========================================

Người phụ trách: [Dev C1]
Nhánh Git: feature/audit-session

API Endpoints:
- GET/POST  /api/audit-sessions/              → AuditSessionListView
- GET/PUT   /api/audit-sessions/<id>/         → AuditSessionDetailView
- POST      /api/audit-sessions/<id>/generate-items/  → generate_items
- POST      /api/audit-sessions/<id>/start/   → start_session
- POST      /api/audit-sessions/<id>/complete/ → complete_session
- GET       /api/audit-sessions/<id>/report/  → export_report
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditSession
from ..serializers import AuditSessionSerializer, AuditSessionDetailSerializer


class AuditSessionListView(generics.ListCreateAPIView):
    """
    GET: Danh sách đợt kiểm kê
    POST: Tạo đợt kiểm kê mới
    
    Query params:
        - status: draft, planned, in_progress, completed, cancelled
        - scope: full, department, location, category, custom
    """
    queryset = AuditSession.objects.all()
    serializer_class = AuditSessionSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset with filtering


class AuditSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Chi tiết đợt kiểm kê
    PUT/PATCH: Cập nhật
    DELETE: Xóa (chỉ khi status=draft)
    """
    queryset = AuditSession.objects.all()
    serializer_class = AuditSessionDetailSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement destroy validation


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_items(request, pk):
    """
    Sinh danh sách tài sản cần kiểm kê theo scope
    
    Output:
        - 200: {"message": "Đã sinh X items", "count": X}
        - 400: Lỗi (đã có items, status không phải draft)
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request, pk):
    """
    Bắt đầu kiểm kê (planned → in_progress)
    
    Output:
        - 200: {"message": "Đã bắt đầu", "session": {...}}
        - 400: Lỗi (status không phải planned)
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_session(request, pk):
    """
    Hoàn thành kiểm kê (in_progress → completed)
    
    Output:
        - 200: {"message": "Hoàn thành", "session": {...}, "summary": {...}}
        - 400: Lỗi (còn items chưa kiểm)
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_report(request, pk):
    """
    Xuất biên bản kiểm kê
    
    Query params:
        - format: xlsx, pdf (mặc định xlsx)
    
    Output:
        - 200: File download
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


__all__ = [
    'AuditSessionListView',
    'AuditSessionDetailView',
    'generate_items',
    'start_session',
    'complete_session',
    'export_report',
]
