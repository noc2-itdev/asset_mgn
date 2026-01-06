"""
AuditItem Views - Chi tiết kiểm kê từng tài sản
================================================

Người phụ trách: [Dev C2]
Nhánh Git: feature/audit-item

API Endpoints:
- GET    /api/audit-sessions/<session_id>/items/    → AuditItemListView
- POST   /api/audit-sessions/<session_id>/add-items/ → add_items_manual
- DELETE /api/audit-sessions/<session_id>/remove-items/ → remove_items
- GET    /api/audit-items/<id>/                     → AuditItemDetailView
- POST   /api/audit-items/<id>/check/               → check_item
- POST   /api/audit-items/<id>/mark-missing/        → mark_missing
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditSession, AuditItem
from ..serializers import AuditItemSerializer, AuditItemCheckSerializer


class AuditItemListView(generics.ListAPIView):
    """
    GET: Danh sách tài sản cần kiểm kê
    
    URL: /api/audit-sessions/<session_id>/items/
    
    Query params:
        - status: pending, matched, missing, ...
    """
    serializer_class = AuditItemSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset


class AuditItemDetailView(generics.RetrieveAPIView):
    """GET: Chi tiết một item kiểm kê"""
    queryset = AuditItem.objects.all()
    serializer_class = AuditItemSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_items_manual(request, session_id):
    """
    Thêm tài sản thủ công vào danh sách
    
    Input: {"asset_ids": [1, 2, 3]}
    Output: {"message": "Đã thêm X items", "count": X}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_items(request, session_id):
    """
    Xóa tài sản khỏi danh sách
    
    Input: {"item_ids": [1, 2, 3]}
    Output: {"message": "Đã xóa X items", "count": X}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_item(request, pk):
    """
    Ghi nhận kết quả kiểm kê
    
    Input: {
        "actual_location_id": 5,
        "actual_status": "in_use",
        "actual_person_id": 3,
        "notes": "...",
        "scanned_code": "QR123"
    }
    
    Output: {
        "item": {...},
        "result_status": "matched|location_mismatch|...",
        "discrepancies": [...]
    }
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_missing(request, pk):
    """
    Đánh dấu không tìm thấy
    
    Input: {"notes": "Lý do"}
    Output: {"item": {...}, "result_status": "missing"}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


__all__ = [
    'AuditItemListView',
    'AuditItemDetailView',
    'add_items_manual',
    'remove_items',
    'check_item',
    'mark_missing',
]
