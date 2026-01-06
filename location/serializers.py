"""Location Serializers"""
from rest_framework import serializers
from main.models import Location


class LocationSerializer(serializers.ModelSerializer):
    assets_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'code', 'description', 'assets_count']
    
    def get_assets_count(self, obj):
        return obj.asset_set.filter(is_deleted=False).count()
