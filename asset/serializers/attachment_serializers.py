"""Attachment Serializers - Dev B3"""
from rest_framework import serializers
from main.models import AssetAttachment


class AssetAttachmentSerializer(serializers.ModelSerializer):
    """File đính kèm"""
    class Meta:
        model = AssetAttachment
        fields = '__all__'
        # TODO: Add file_name, file_size


__all__ = ['AssetAttachmentSerializer']
