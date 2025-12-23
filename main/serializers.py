from rest_framework import serializers
from .models import Department, Person, AssetCategory, Asset, AssetHistory, TicketRequest, AssetAudit, Location, \
    AssetAttachment


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Person
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'


class AssetAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAttachment
        fields = '__all__'


class AssetComponentSerializer(serializers.ModelSerializer):
    """Serializer cho linh kiện của tài sản"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Asset
        fields = ['id', 'name', 'asset_code', 'category', 'category_name', 'status']


class AssetSerializer(serializers.ModelSerializer):
    """Serializer cho tài sản chính"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_department_name = serializers.CharField(source='current_department.name', read_only=True)
    current_person_name = serializers.CharField(source='current_person.name', read_only=True)
    components = AssetComponentSerializer(many=True, read_only=True)
    parent_asset_name = serializers.CharField(source='parent_asset.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    attachments = AssetAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['qr_code']


class AssetCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer đặc biệt cho tạo/cập nhật tài sản"""

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['qr_code']

    def validate_parent_asset(self, value):
        # Kiểm tra tài sản không thể là cha của chính nó
        if value and self.instance and value.id == self.instance.id:
            raise serializers.ValidationError("Tài sản không thể thuộc về chính nó.")
        return value


class AssetHistorySerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    from_department_name = serializers.CharField(source='from_department.name', read_only=True)
    to_department_name = serializers.CharField(source='to_department.name', read_only=True)
    from_person_name = serializers.CharField(source='from_person.name', read_only=True)
    to_person_name = serializers.CharField(source='to_person.name', read_only=True)
    from_location_name = serializers.CharField(source='from_location.name', read_only=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True)
    related_ticket_id = serializers.CharField(source='related_ticket.id', read_only=True)
    related_audit_id = serializers.CharField(source='related_audit.id', read_only=True)

    class Meta:
        model = AssetHistory
        fields = '__all__'


class TicketRequestSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    requester_name = serializers.CharField(source='requester.get_full_name', read_only=True)
    handler_name = serializers.CharField(source='handler.get_full_name', read_only=True)

    class Meta:
        model = TicketRequest
        fields = '__all__'
        read_only_fields = ['requester']


class AssetAuditSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    auditor_name = serializers.CharField(source='auditor.get_full_name', read_only=True)
    physical_location_name = serializers.CharField(source='physical_location.name', read_only=True)

    class Meta:
        model = AssetAudit
        fields = '__all__'
