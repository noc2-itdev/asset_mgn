"""
Asset Serializers
=================

Người phụ trách: [Dev B1]
"""

from rest_framework import serializers
from main.models import Asset, AssetHistory


class AssetSerializer(serializers.ModelSerializer):
    """Serializer cho danh sách Asset"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    department_name = serializers.CharField(source='current_department.name', read_only=True)
    person_name = serializers.CharField(source='current_person.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'asset_code', 'status',
            'category', 'category_name',
            'current_department', 'department_name',
            'current_person', 'person_name',
            'location', 'location_name',
            'serial_number', 'model', 'vendor', 'value'
        ]


class AssetDetailSerializer(serializers.ModelSerializer):
    """Serializer chi tiết cho Asset"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    department_name = serializers.CharField(source='current_department.name', read_only=True)
    person_name = serializers.CharField(source='current_person.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    parent_asset_code = serializers.CharField(source='parent_asset.asset_code', read_only=True)
    components_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'qr_code', 'is_deleted', 'deleted_at', 'deleted_by']
    
    def get_components_count(self, obj):
        return obj.components.filter(is_deleted=False).count()


class AssetHistorySerializer(serializers.ModelSerializer):
    """Serializer cho lịch sử tài sản"""
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    from_department_name = serializers.CharField(source='from_department.name', read_only=True)
    to_department_name = serializers.CharField(source='to_department.name', read_only=True)
    from_person_name = serializers.CharField(source='from_person.name', read_only=True)
    to_person_name = serializers.CharField(source='to_person.name', read_only=True)
    
    class Meta:
        model = AssetHistory
        fields = [
            'id', 'date', 'action', 'action_display',
            'from_department', 'from_department_name',
            'to_department', 'to_department_name',
            'from_person', 'from_person_name',
            'to_person', 'to_person_name',
            'note'
        ]


__all__ = ['AssetSerializer', 'AssetDetailSerializer', 'AssetHistorySerializer']
