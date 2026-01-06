"""Department Serializers"""
from rest_framework import serializers
from main.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    assets_count = serializers.SerializerMethodField()
    persons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'assets_count', 'persons_count']
    
    def get_assets_count(self, obj):
        return obj.asset_set.filter(is_deleted=False).count()
    
    def get_persons_count(self, obj):
        return obj.person_set.count()
