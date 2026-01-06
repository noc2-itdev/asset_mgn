"""
Transfer Views - Bàn giao và điều chuyển tài sản
================================================

Người phụ trách: [Dev B3]
Nhánh Git: feature/asset-transfer

API Endpoints:
- POST   /api/assets/<id>/transfer/    → transfer_asset
- GET    /api/assets/<id>/attachments/ → AssetAttachmentListView
- POST   /api/assets/<id>/attachments/ → AssetAttachmentListView
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Asset, AssetAttachment, AssetHistory, AssetAction, Department, Person, Location
from ..serializers import AssetSerializer, AssetAttachmentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_asset(request, pk):
    """
    Bàn giao tài sản cho người/phòng ban khác
    
    URL: /api/assets/<id>/transfer/
    
    Input (JSON):
        {
            "to_department_id": 5,    // Phòng ban nhận (optional)
            "to_person_id": 3,        // Người nhận (optional)
            "to_location_id": 2,      // Vị trí mới (optional)
            "notes": "Bàn giao theo QĐ số..."  // Ghi chú
        }
    
    Output:
        - 200: {
            "message": "Đã bàn giao thành công",
            "asset": {...},
            "changes": {
                "department": "Phòng A → Phòng B",
                "person": "Nguyễn A → Trần B",
                "location": "Tầng 1 → Tầng 2"
            }
        }
        - 400: Lỗi validation
        - 404: Không tìm thấy asset
    
    Logic:
        1. Lưu thông tin cũ (from_department, from_person, from_location)
        2. Cập nhật current_department, current_person, location
        3. Ghi AssetHistory action=TRANSFER với đầy đủ thông tin
        4. Trả về changes
    """
    # TODO: Implement
    to_department_id = request.data.get('to_department_id')
    to_person_id = request.data.get('to_person_id')
    to_location_id = request.data.get('to_location_id')
    notes = request.data.get('notes', '')
    
    try:
        asset = Asset.active_objects.get(pk=pk)
        
        # Lưu thông tin cũ
        from_department = asset.current_department
        from_person = asset.current_person
        from_location = asset.location
        
        changes = {}
        
        # Cập nhật department
        if to_department_id:
            to_department = Department.objects.get(pk=to_department_id)
            if from_department != to_department:
                changes['department'] = f"{from_department.name if from_department else 'N/A'} → {to_department.name}"
                asset.current_department = to_department
        
        # Cập nhật person
        if to_person_id:
            to_person = Person.objects.get(pk=to_person_id)
            if from_person != to_person:
                changes['person'] = f"{from_person.name if from_person else 'N/A'} → {to_person.name}"
                asset.current_person = to_person
        
        # Cập nhật location
        if to_location_id:
            to_location = Location.objects.get(pk=to_location_id)
            if from_location != to_location:
                changes['location'] = f"{from_location.name if from_location else 'N/A'} → {to_location.name}"
                asset.location = to_location
        
        if not changes:
            return Response(
                {"error": "Không có thay đổi nào"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        asset.save()
        
        # Ghi history
        AssetHistory.objects.create(
            asset=asset,
            action=AssetAction.TRANSFER,
            from_department=from_department,
            to_department=asset.current_department,
            from_person=from_person,
            to_person=asset.current_person,
            from_location=from_location,
            to_location=asset.location,
            note=notes
        )
        
        return Response({
            "message": "Đã bàn giao thành công",
            "asset": AssetSerializer(asset).data,
            "changes": changes
        })
        
    except Asset.DoesNotExist:
        return Response(
            {"error": "Không tìm thấy tài sản"},
            status=status.HTTP_404_NOT_FOUND
        )
    except (Department.DoesNotExist, Person.DoesNotExist, Location.DoesNotExist) as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


class AssetAttachmentListView(generics.ListCreateAPIView):
    """
    GET: Danh sách file đính kèm của tài sản
    POST: Upload file đính kèm mới
    
    URL: /api/assets/<id>/attachments/
    
    Input (POST - multipart/form-data):
        - file: File cần upload
        - description: Mô tả (optional)
    
    Response:
        - 200: Danh sách attachments
        - 201: Attachment mới
    """
    serializer_class = AssetAttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        asset_id = self.kwargs.get('pk')
        return AssetAttachment.objects.filter(asset_id=asset_id)
    
    def perform_create(self, serializer):
        asset_id = self.kwargs.get('pk')
        asset = Asset.active_objects.get(pk=asset_id)
        serializer.save(asset=asset)


# Export
__all__ = [
    'transfer_asset',
    'AssetAttachmentListView',
]
