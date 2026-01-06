"""
AuditAction Views - Đề xuất xử lý chênh lệch
=============================================

Người phụ trách: [Dev C3]
Nhánh Git: feature/audit-action

API Endpoints:
- GET/POST  /api/audit-items/<item_id>/actions/  → AuditActionListView
- GET       /api/audit-actions/<id>/             → AuditActionDetailView
- POST      /api/audit-actions/<id>/approve/     → approve_action
- POST      /api/audit-actions/<id>/reject/      → reject_action
- POST      /api/audit-actions/<id>/execute/     → execute_action
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditItem, AuditAction
from ..serializers import AuditActionSerializer


class AuditActionListView(generics.ListCreateAPIView):
    """
    GET: Danh sách đề xuất xử lý cho 1 item
    POST: Tạo đề xuất mới
    
    Input (POST): {"action_type": "update_location|repair|...", "description": "..."}
    """
    serializer_class = AuditActionSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset and perform_create


class AuditActionDetailView(generics.RetrieveAPIView):
    """GET: Chi tiết đề xuất"""
    queryset = AuditAction.objects.all()
    serializer_class = AuditActionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_action(request, pk):
    """
    Duyệt đề xuất
    
    Output: {"message": "Đã duyệt", "action": {...}}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_action(request, pk):
    """
    Từ chối đề xuất
    
    Input: {"reason": "Lý do từ chối"}
    Output: {"message": "Đã từ chối", "action": {...}}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_action(request, pk):
    """
    Thực hiện đề xuất đã duyệt
    
    Output: {
        "message": "Đã thực hiện",
        "action": {...},
        "changes": {"asset_updated": true, ...}
    }
    
    Logic theo action_type:
        - update_location: Cập nhật Asset.location
        - update_status: Cập nhật Asset.status
        - repair: Tạo TicketRequest
        - liquidate: Asset.status = LIQUIDATED
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


__all__ = [
    'AuditActionListView',
    'AuditActionDetailView',
    'approve_action',
    'reject_action',
    'execute_action',
]
