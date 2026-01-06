"""Department Serializers"""
from rest_framework import serializers
from main.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        # TODO: Add assets_count, persons_count
