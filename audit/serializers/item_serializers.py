"""
AuditItem Serializers
=====================
Người phụ trách: [Dev C2]
"""
from rest_framework import serializers
from main.models import AuditItem


class AuditItemSerializer(serializers.ModelSerializer):
    """Item kiểm kê với expected/actual values"""
    class Meta:
        model = AuditItem
        fields = '__all__'
        # TODO: Add asset info, location names


class AuditItemCheckSerializer(serializers.Serializer):
    """Input để ghi nhận kết quả kiểm kê"""
    actual_location_id = serializers.IntegerField(required=False, allow_null=True)
    actual_status = serializers.CharField(required=True)
    actual_person_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    scanned_code = serializers.CharField(required=False, allow_blank=True)
    # TODO: Add validation


__all__ = ['AuditItemSerializer', 'AuditItemCheckSerializer']
