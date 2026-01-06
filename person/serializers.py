"""Person Serializers"""
from rest_framework import serializers
from main.models import Person


class PersonSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    assets_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ['id', 'name', 'code', 'email', 'phone', 'position', 
                  'department', 'department_name', 'assets_count']
    
    def get_assets_count(self, obj):
        return obj.asset_set.filter(is_deleted=False).count()
