"""
AuditAction Views - Đề xuất xử lý chênh lệch
=============================================

Người phụ trách: [Dev C3]
Nhánh Git: feature/audit-action

API Endpoints:
- GET    /api/audit-items/<item_id>/actions/     → AuditActionListView
- POST   /api/audit-items/<item_id>/actions/     → AuditActionListView
- GET    /api/audit-actions/<id>/                → AuditActionDetailView
- POST   /api/audit-actions/<id>/approve/        → approve_action
- POST   /api/audit-actions/<id>/reject/         → reject_action
- POST   /api/audit-actions/<id>/execute/        → execute_action
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditItem, AuditAction, AuditActionType, AuditActionStatus
from ..serializers import AuditActionSerializer


class AuditActionListView(generics.ListCreateAPIView):
    """
    GET: Danh sách đề xuất xử lý cho 1 item kiểm kê
    POST: Tạo đề xuất xử lý mới
    
    URL: /api/audit-items/<item_id>/actions/
    
    Input (POST):
        {
            "action_type": "update_location|repair|report_missing|...",
            "description": "Mô tả chi tiết đề xuất"
        }
    
    Response:
        - 200: Danh sách AuditAction
        - 201: AuditAction mới được tạo
    """
    serializer_class = AuditActionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        item_id = self.kwargs.get('item_id')
        return AuditAction.objects.filter(audit_item_id=item_id)
    
    def perform_create(self, serializer):
        item_id = self.kwargs.get('item_id')
        item = AuditItem.objects.get(pk=item_id)
        serializer.save(
            audit_item=item,
            proposed_by=self.request.user
        )


class AuditActionDetailView(generics.RetrieveAPIView):
    """
    GET: Chi tiết một đề xuất xử lý
    
    Response:
        - 200: AuditAction với thông tin item, asset
        - 404: Không tìm thấy
    """
    queryset = AuditAction.objects.all()
    serializer_class = AuditActionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_action(request, pk):
    """
    Duyệt đề xuất xử lý
    
    Input: Không cần body (hoặc optional notes)
    
    Output:
        - 200: {"message": "Đã duyệt", "action": {...}}
        - 400: Lỗi (status không phải pending)
        - 404: Không tìm thấy action
    
    Logic:
        1. Kiểm tra action.status == pending
        2. Gọi action.approve(approved_by=request.user)
        3. Trả về action đã cập nhật
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_action(request, pk):
    """
    Từ chối đề xuất xử lý
    
    Input (JSON):
        {
            "reason": "Lý do từ chối"  // Bắt buộc
        }
    
    Output:
        - 200: {"message": "Đã từ chối", "action": {...}}
        - 400: Lỗi (thiếu reason, status không phải pending)
        - 404: Không tìm thấy action
    
    Logic:
        1. Kiểm tra action.status == pending
        2. Gọi action.reject(rejected_by=request.user, reason=reason)
        3. Trả về action đã cập nhật
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_action(request, pk):
    """
    Thực hiện đề xuất đã duyệt
    
    Input: Không cần body
    
    Output:
        - 200: {
            "message": "Đã thực hiện",
            "action": {...},
            "changes": {
                "asset_updated": true,
                "ticket_created": {...}  // Nếu action_type=repair
            }
        }
        - 400: Lỗi (status không phải approved)
        - 404: Không tìm thấy action
    
    Logic theo action_type:
        - update_location: Cập nhật Asset.location
        - update_status: Cập nhật Asset.status
        - update_person: Cập nhật Asset.current_person
        - report_missing: Cập nhật Asset.status = LOST
        - repair: Tạo TicketRequest(request_type='repair')
        - liquidate: Cập nhật Asset.status = LIQUIDATED
        - create_new: Tạo Asset mới (cho tài sản thừa)
    """
    # TODO: Implement
    pass


# Export tất cả
__all__ = [
    'AuditActionListView',
    'AuditActionDetailView',
    'approve_action',
    'reject_action',
    'execute_action',
]
