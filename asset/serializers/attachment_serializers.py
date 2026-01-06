"""
Attachment Serializers
======================

Người phụ trách: [Dev B3]
"""

from rest_framework import serializers
from main.models import AssetAttachment


class AssetAttachmentSerializer(serializers.ModelSerializer):
    """Serializer cho file đính kèm"""
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = AssetAttachment
        fields = ['id', 'asset', 'file', 'file_name', 'file_size', 'description', 'uploaded_at']
        read_only_fields = ['id', 'asset', 'uploaded_at']
    
    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1] if obj.file else None
    
    def get_file_size(self, obj):
        try:
            return obj.file.size
        except:
            return None


__all__ = ['AssetAttachmentSerializer']
