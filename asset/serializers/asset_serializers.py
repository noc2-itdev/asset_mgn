"""Asset Serializers - Dev B1"""
from rest_framework import serializers
from main.models import Asset, AssetHistory


class AssetSerializer(serializers.ModelSerializer):
    """List view: basic info + computed fields"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    department_name = serializers.CharField(source='current_department.name', read_only=True)
    person_name = serializers.CharField(source='current_person.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'asset_code', 'internal_code', 'status',
            'category', 'category_name',
            'current_department', 'department_name',
            'current_person', 'person_name',
            'location', 'location_name',
            'unit', 'quantity',
            'serial_number', 'model', 'vendor',
            'original_value', 'total_value'
        ]
        # TODO: Add total_value as SerializerMethodField


class AssetDetailSerializer(serializers.ModelSerializer):
    """Detail view: all fields + computed + nested"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    department_name = serializers.CharField(source='current_department.name', read_only=True)
    person_name = serializers.CharField(source='current_person.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    parent_asset_code = serializers.CharField(source='parent_asset.asset_code', read_only=True)
    components_count = serializers.SerializerMethodField()
    residual_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_component = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'qr_code', 'is_deleted', 'deleted_at', 'deleted_by']
    
    def get_components_count(self, obj):
        # TODO: Implement
        pass


class AssetHistorySerializer(serializers.ModelSerializer):
    """Lịch sử biến động"""
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AssetHistory
        fields = '__all__'
        # TODO: Add from/to names


class AssetSplitSerializer(serializers.Serializer):
    """Input cho tách lô tài sản"""
    split_quantity = serializers.IntegerField(min_value=1, help_text="Số lượng cần tách")
    reason = serializers.CharField(required=False, allow_blank=True, help_text="Lý do tách")
    new_status = serializers.CharField(required=False, allow_blank=True, help_text="Trạng thái mới")
    new_asset_code = serializers.CharField(required=False, allow_blank=True, help_text="Mã TS mới (tự sinh nếu bỏ trống)")


__all__ = ['AssetSerializer', 'AssetDetailSerializer', 'AssetHistorySerializer', 'AssetSplitSerializer']
