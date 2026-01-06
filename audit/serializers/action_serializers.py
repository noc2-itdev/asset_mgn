"""
AuditAction Serializers
=======================

Người phụ trách: [Dev C3]
"""

from rest_framework import serializers
from main.models import AuditAction, AuditActionType, AuditActionStatus


class AuditActionSerializer(serializers.ModelSerializer):
    """
    Serializer cho AuditAction
    
    Fields:
        - id, action_type, description, status
        - proposed_by, approved_by, executed_by (names)
        - proposed_at, approved_at, executed_at
        - rejection_reason
    """
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    proposed_by_name = serializers.CharField(source='proposed_by.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    executed_by_name = serializers.CharField(source='executed_by.username', read_only=True)
    
    class Meta:
        model = AuditAction
        fields = [
            'id', 'audit_item',
            'action_type', 'action_type_display',
            'description',
            'status', 'status_display',
            'proposed_by', 'proposed_by_name', 'proposed_at',
            'approved_by', 'approved_by_name', 'approved_at',
            'executed_by', 'executed_by_name', 'executed_at',
            'rejection_reason'
        ]
        read_only_fields = [
            'id', 'audit_item', 'status',
            'proposed_by', 'proposed_at',
            'approved_by', 'approved_at',
            'executed_by', 'executed_at',
            'rejection_reason'
        ]


class AuditActionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo đề xuất xử lý mới
    
    Input:
        - action_type: Loại hành động (update_location, repair, ...)
        - description: Mô tả chi tiết đề xuất
    """
    class Meta:
        model = AuditAction
        fields = ['action_type', 'description']
    
    def validate_action_type(self, value):
        valid_types = [choice[0] for choice in AuditActionType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Loại hành động không hợp lệ. Chọn một trong: {valid_types}"
            )
        return value


class AuditActionRejectSerializer(serializers.Serializer):
    """
    Serializer để từ chối đề xuất
    
    Input:
        - reason: Lý do từ chối (bắt buộc)
    """
    reason = serializers.CharField(required=True, min_length=10)
    
    def validate_reason(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Lý do từ chối phải có ít nhất 10 ký tự"
            )
        return value.strip()


# Export
__all__ = [
    'AuditActionSerializer',
    'AuditActionCreateSerializer',
    'AuditActionRejectSerializer',
]
