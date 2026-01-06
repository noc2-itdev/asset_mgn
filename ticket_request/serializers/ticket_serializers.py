"""Ticket Serializers - Dev D1"""
from rest_framework import serializers
from main.models import TicketRequest


class TicketRequestSerializer(serializers.ModelSerializer):
    """Yêu cầu sửa chữa/bảo trì"""
    class Meta:
        model = TicketRequest
        fields = '__all__'
        # TODO: Add asset info, status_display


__all__ = ['TicketRequestSerializer']
