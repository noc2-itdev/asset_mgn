"""Asset Serializers - Dev B1"""
from rest_framework import serializers
from main.models import Asset, AssetHistory


class AssetSerializer(serializers.ModelSerializer):
    """List view: basic info"""
    class Meta:
        model = Asset
        fields = ['id', 'name', 'asset_code', 'status', 'category', 
                  'current_department', 'current_person', 'location']
        # TODO: Add display names


class AssetDetailSerializer(serializers.ModelSerializer):
    """Detail view: all fields + computed"""
    class Meta:
        model = Asset
        fields = '__all__'
        # TODO: Add components_count, nested info


class AssetHistorySerializer(serializers.ModelSerializer):
    """Lịch sử biến động"""
    class Meta:
        model = AssetHistory
        fields = '__all__'
        # TODO: Add action_display, names


__all__ = ['AssetSerializer', 'AssetDetailSerializer', 'AssetHistorySerializer']
