"""
Transfer Views - Bàn giao và đính kèm
=====================================

Người phụ trách: [Dev B3]
Nhánh Git: feature/asset-transfer

API Endpoints:
- POST     /api/assets/<id>/transfer/     → transfer_asset
- GET/POST /api/assets/<id>/attachments/  → AssetAttachmentListView
"""

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main.models import Asset, AssetAttachment
from ..serializers import AssetAttachmentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_asset(request, pk):
    """
    Bàn giao tài sản
    
    Input: {
        "to_department_id": 5,
        "to_person_id": 3,
        "to_location_id": 2,
        "notes": "..."
    }
    
    Output: {
        "message": "Đã bàn giao",
        "asset": {...},
        "changes": {"department": "A → B", ...}
    }
    
    Logic:
        - Lưu from_* values
        - Update current_department, current_person, location
        - Log AssetHistory action=TRANSFER
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


class AssetAttachmentListView(generics.ListCreateAPIView):
    """
    GET: Danh sách file đính kèm
    POST: Upload file mới (multipart/form-data)
    """
    serializer_class = AssetAttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset and perform_create


__all__ = ['transfer_asset', 'AssetAttachmentListView']
