"""
AuditSession Serializers
========================

Người phụ trách: [Dev C1]
"""

from rest_framework import serializers
from main.models import AuditSession, Department, Location, AssetCategory


class AuditSessionSerializer(serializers.ModelSerializer):
    """
    Serializer cho danh sách AuditSession
    
    Fields:
        - id, code, name, scope, status
        - planned_start_date, planned_end_date
        - total_items, checked_items, progress_percent
        - created_by (name only)
    """
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    progress_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = AuditSession
        fields = [
            'id', 'code', 'name', 'scope', 'status',
            'planned_start_date', 'planned_end_date',
            'total_items', 'checked_items', 'progress_percent',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'code', 'status', 'total_items', 'checked_items', 'created_at']


class AuditSessionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer chi tiết cho AuditSession
    
    Bao gồm thêm:
        - scope_department, scope_location, scope_category (nested)
        - approved_by, statistics
        - items summary (matched, missing, mismatch counts)
    """
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    scope_department_name = serializers.CharField(source='scope_department.name', read_only=True)
    scope_location_name = serializers.CharField(source='scope_location.name', read_only=True)
    scope_category_name = serializers.CharField(source='scope_category.name', read_only=True)
    progress_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = AuditSession
        fields = '__all__'
        read_only_fields = [
            'id', 'code', 'created_at', 'started_at', 'completed_at',
            'total_items', 'checked_items', 'matched_items', 'mismatched_items'
        ]


class AuditSessionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo AuditSession mới
    
    Required fields:
        - name: Tên đợt kiểm kê
        - scope: Phạm vi (full, department, location, category, custom)
    
    Optional fields:
        - description, planned_start_date, planned_end_date
        - scope_department, scope_location, scope_category (tùy scope)
    """
    class Meta:
        model = AuditSession
        fields = [
            'name', 'description', 'scope',
            'scope_department', 'scope_location', 'scope_category',
            'planned_start_date', 'planned_end_date'
        ]
    
    def validate(self, data):
        """
        Validate scope và các trường liên quan
        - scope=department → scope_department bắt buộc
        - scope=location → scope_location bắt buộc
        - scope=category → scope_category bắt buộc
        """
        scope = data.get('scope')
        
        if scope == 'department' and not data.get('scope_department'):
            raise serializers.ValidationError({
                'scope_department': 'Phải chọn phòng ban khi scope=department'
            })
        
        # TODO: Validate cho location, category
        
        return data


# Export
__all__ = [
    'AuditSessionSerializer',
    'AuditSessionDetailSerializer',
    'AuditSessionCreateSerializer',
]
