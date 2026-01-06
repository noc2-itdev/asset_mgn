"""
AuditSession Views - Quản lý đợt kiểm kê
=========================================

Người phụ trách: [Dev C1]
Nhánh Git: feature/audit-session

API Endpoints:
- GET    /api/audit-sessions/              → AuditSessionListView
- POST   /api/audit-sessions/              → AuditSessionListView
- GET    /api/audit-sessions/<id>/         → AuditSessionDetailView
- PUT    /api/audit-sessions/<id>/         → AuditSessionDetailView
- DELETE /api/audit-sessions/<id>/         → AuditSessionDetailView
- POST   /api/audit-sessions/<id>/generate-items/  → generate_items
- POST   /api/audit-sessions/<id>/start/   → start_session
- POST   /api/audit-sessions/<id>/complete/ → complete_session
- GET    /api/audit-sessions/<id>/report/  → export_report
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditSession, AuditSessionStatus
from ..serializers import AuditSessionSerializer, AuditSessionDetailSerializer


class AuditSessionListView(generics.ListCreateAPIView):
    """
    GET: Danh sách các đợt kiểm kê
    POST: Tạo đợt kiểm kê mới
    
    Query params:
        - status: Lọc theo trạng thái (draft, planned, in_progress, completed, cancelled)
        - scope: Lọc theo phạm vi (full, department, location, category, custom)
    
    Response:
        - 200: Danh sách AuditSession
        - 201: AuditSession mới được tạo
    """
    queryset = AuditSession.objects.all()
    serializer_class = AuditSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # TODO: Implement filtering by status, scope
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')


class AuditSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Chi tiết đợt kiểm kê
    PUT/PATCH: Cập nhật thông tin đợt kiểm kê
    DELETE: Xóa đợt kiểm kê (chỉ khi status=draft)
    
    Response:
        - 200: AuditSession detail
        - 400: Không thể xóa (status != draft)
        - 404: Không tìm thấy
    """
    queryset = AuditSession.objects.all()
    serializer_class = AuditSessionDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        # TODO: Chỉ cho phép xóa khi status=draft
        instance = self.get_object()
        if instance.status != AuditSessionStatus.DRAFT:
            return Response(
                {"error": "Chỉ có thể xóa đợt kiểm kê ở trạng thái Nháp"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_items(request, pk):
    """
    Tự động sinh danh sách tài sản cần kiểm kê dựa trên scope
    
    Input: Không cần body (dựa trên scope đã thiết lập)
    
    Output:
        - 200: {"message": "Đã sinh X items", "count": X}
        - 400: Lỗi (đã có items, status không phải draft)
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra session tồn tại và status=draft
        2. Gọi session.generate_items()
        3. Trả về số lượng items đã sinh
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request, pk):
    """
    Bắt đầu thực hiện kiểm kê (chuyển status từ planned → in_progress)
    
    Input: Không cần body
    
    Output:
        - 200: {"message": "Đã bắt đầu kiểm kê", "session": {...}}
        - 400: Lỗi (status không phải planned)
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra session.status == planned
        2. Cập nhật status = in_progress, started_at = now()
        3. Trả về session đã cập nhật
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_session(request, pk):
    """
    Hoàn thành đợt kiểm kê (chuyển status từ in_progress → completed)
    
    Input: Không cần body
    
    Output:
        - 200: {"message": "Đã hoàn thành", "session": {...}, "summary": {...}}
        - 400: Lỗi (status không phải in_progress, còn items chưa kiểm)
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra tất cả items đã được kiểm
        2. Cập nhật status = completed, completed_at = now()
        3. Gọi session.update_statistics()
        4. Trả về session và thống kê
    """
    # TODO: Implement
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_report(request, pk):
    """
    Xuất biên bản kiểm kê
    
    Query params:
        - format: xlsx, pdf (mặc định xlsx)
    
    Output:
        - 200: File download
        - 400: Chưa hoàn thành kiểm kê
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra session.status == completed
        2. Tạo file Excel/PDF với template
        3. Trả về file download
    """
    # TODO: Implement
    pass


# Export tất cả
__all__ = [
    'AuditSessionListView',
    'AuditSessionDetailView',
    'generate_items',
    'start_session',
    'complete_session',
    'export_report',
]
