"""
Component Views - Quản lý linh kiện
===================================

Người phụ trách: [Dev B2]
Nhánh Git: feature/asset-component

API Endpoints:
- GET   /api/assets/<id>/components/  → AssetComponentListView
- POST  /api/assets/<id>/upgrade/     → upgrade_component
- POST  /api/assets/<id>/retrieve/    → retrieve_component
"""

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main.models import Asset
from ..serializers import AssetSerializer


class AssetComponentListView(generics.ListAPIView):
    """GET: Danh sách linh kiện của tài sản (parent_asset = this)"""
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_component(request, pk):
    """
    Lắp linh kiện vào tài sản
    
    Input: {"component_id": 5, "notes": "..."}
    Output: {"message": "...", "asset": {...}, "component": {...}}
    
    Logic:
        - Validate component.category.is_component = true
        - Validate component.parent_asset = null
        - Set component.parent_asset = asset
        - Log AssetHistory action=UPGRADE
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retrieve_component(request, pk):
    """
    Tháo linh kiện khỏi tài sản
    
    Input: {"component_id": 5, "notes": "...", "new_parent_id": 10}
    Output: {"message": "...", "asset": {...}, "component": {...}}
    
    Logic:
        - Validate component.parent_asset = asset
        - Set component.parent_asset = new_parent hoặc null
        - Log AssetHistory action=RETRIEVE
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


__all__ = ['AssetComponentListView', 'upgrade_component', 'retrieve_component']
