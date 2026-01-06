"""
Ticket Request Serializers
==========================

Người phụ trách: [Dev D1]
"""

from rest_framework import serializers
from main.models import TicketRequest


class TicketRequestSerializer(serializers.ModelSerializer):
    """Serializer cho danh sách Ticket"""
    asset_code = serializers.CharField(source='asset.asset_code', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    requester_name = serializers.CharField(source='requester.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TicketRequest
        fields = [
            'id', 'asset', 'asset_code', 'asset_name',
            'request_type', 'status', 'status_display',
            'requester', 'requester_name',
            'requested_at', 'title'
        ]
        read_only_fields = ['id', 'requester', 'requested_at', 'status']


class TicketRequestDetailSerializer(serializers.ModelSerializer):
    """Serializer chi tiết cho Ticket"""
    asset_code = serializers.CharField(source='asset.asset_code', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    requester_name = serializers.CharField(source='requester.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = TicketRequest
        fields = '__all__'
        read_only_fields = [
            'id', 'requester', 'requested_at', 'status',
            'approved_by', 'approved_at', 'completed_at'
        ]


__all__ = ['TicketRequestSerializer', 'TicketRequestDetailSerializer']
