"""
AuditSession Serializers
========================
Người phụ trách: [Dev C1]
"""
from rest_framework import serializers
from main.models import AuditSession


class AuditSessionSerializer(serializers.ModelSerializer):
    """List serializer: id, code, name, scope, status, progress"""
    class Meta:
        model = AuditSession
        fields = ['id', 'code', 'name', 'scope', 'status', 'total_items', 'checked_items']
        # TODO: Add computed fields


class AuditSessionDetailSerializer(serializers.ModelSerializer):
    """Detail serializer: all fields + nested info"""
    class Meta:
        model = AuditSession
        fields = '__all__'
        # TODO: Add nested serializers


__all__ = ['AuditSessionSerializer', 'AuditSessionDetailSerializer']
