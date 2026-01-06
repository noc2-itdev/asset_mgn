"""Location Serializers"""
from rest_framework import serializers
from main.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        # TODO: Add assets_count
