"""
AuditAction Serializers
=======================
Người phụ trách: [Dev C3]
"""
from rest_framework import serializers
from main.models import AuditAction


class AuditActionSerializer(serializers.ModelSerializer):
    """Đề xuất xử lý chênh lệch"""
    class Meta:
        model = AuditAction
        fields = '__all__'
        # TODO: Add display names


__all__ = ['AuditActionSerializer']
