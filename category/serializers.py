"""AssetCategory Serializers"""
from rest_framework import serializers
from main.models import AssetCategory


class AssetCategorySerializer(serializers.ModelSerializer):
    assets_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AssetCategory
        fields = ['id', 'name', 'code', 'description', 'is_component', 'assets_count']
    
    def get_assets_count(self, obj):
        return obj.asset_set.filter(is_deleted=False).count()
