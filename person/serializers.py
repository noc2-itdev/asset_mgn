"""Person Serializers"""
from rest_framework import serializers
from main.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        # TODO: Add department_name, assets_count
