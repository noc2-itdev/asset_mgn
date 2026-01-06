"""
AuditItem Serializers
=====================

Người phụ trách: [Dev C2]
"""

from rest_framework import serializers
from main.models import AuditItem, Asset, Location, Person


class AuditItemSerializer(serializers.ModelSerializer):
    """
    Serializer cho danh sách AuditItem
    
    Fields:
        - id, asset (code, name), result_status
        - expected_location, actual_location
        - expected_status, actual_status
        - checked_at, checked_by
    """
    asset_code = serializers.CharField(source='asset.asset_code', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    expected_location_name = serializers.CharField(source='expected_location.name', read_only=True)
    actual_location_name = serializers.CharField(source='actual_location.name', read_only=True)
    expected_person_name = serializers.CharField(source='expected_person.name', read_only=True)
    actual_person_name = serializers.CharField(source='actual_person.name', read_only=True)
    checked_by_name = serializers.CharField(source='checked_by.username', read_only=True)
    
    class Meta:
        model = AuditItem
        fields = [
            'id', 'asset', 'asset_code', 'asset_name',
            'result_status',
            'expected_location', 'expected_location_name',
            'actual_location', 'actual_location_name',
            'expected_status', 'actual_status',
            'expected_person', 'expected_person_name',
            'actual_person', 'actual_person_name',
            'checked_at', 'checked_by', 'checked_by_name',
            'notes'
        ]
        read_only_fields = ['id', 'asset', 'result_status', 'checked_at']


class AuditItemCheckSerializer(serializers.Serializer):
    """
    Serializer để ghi nhận kết quả kiểm kê
    
    Input fields:
        - actual_location_id: ID vị trí thực tế (optional)
        - actual_status: Trạng thái thực tế (required)
        - actual_person_id: ID người quản lý thực tế (optional)
        - notes: Ghi chú (optional)
        - scanned_code: Mã QR/Barcode đã quét (optional)
    """
    actual_location_id = serializers.IntegerField(required=False, allow_null=True)
    actual_status = serializers.CharField(required=True)
    actual_person_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    scanned_code = serializers.CharField(required=False, allow_blank=True)
    
    def validate_actual_location_id(self, value):
        if value:
            if not Location.objects.filter(id=value).exists():
                raise serializers.ValidationError("Vị trí không tồn tại")
        return value
    
    def validate_actual_person_id(self, value):
        if value:
            if not Person.objects.filter(id=value).exists():
                raise serializers.ValidationError("Người quản lý không tồn tại")
        return value


class AuditItemAddSerializer(serializers.Serializer):
    """
    Serializer để thêm tài sản thủ công vào danh sách kiểm kê
    
    Input:
        - asset_ids: List[int] - Danh sách ID tài sản
    """
    asset_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    
    def validate_asset_ids(self, value):
        # Kiểm tra các asset tồn tại
        existing_ids = set(Asset.objects.filter(id__in=value).values_list('id', flat=True))
        invalid_ids = set(value) - existing_ids
        
        if invalid_ids:
            raise serializers.ValidationError(
                f"Không tìm thấy các tài sản với ID: {list(invalid_ids)}"
            )
        
        return value


# Export
__all__ = [
    'AuditItemSerializer',
    'AuditItemCheckSerializer',
    'AuditItemAddSerializer',
]
