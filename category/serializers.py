"""AssetCategory Serializers"""
from rest_framework import serializers
from main.models import AssetCategory


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'
        # TODO: Add assets_count
