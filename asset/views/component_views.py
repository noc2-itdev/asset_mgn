"""
Component Views - Quản lý linh kiện
===================================

Người phụ trách: [Dev B2]
Nhánh Git: feature/asset-component

API Endpoints:
- GET    /api/assets/<id>/components/     → AssetComponentListView
- POST   /api/assets/<id>/upgrade/        → upgrade_component
- POST   /api/assets/<id>/retrieve/       → retrieve_component
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Asset, AssetHistory, AssetAction
from ..serializers import AssetSerializer


class AssetComponentListView(generics.ListAPIView):
    """
    GET: Danh sách linh kiện của tài sản
    
    URL: /api/assets/<id>/components/
    
    Response:
        - 200: Danh sách các Asset là component của tài sản này
              (các asset có parent_asset = asset hiện tại)
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        asset_id = self.kwargs.get('pk')
        return Asset.active_objects.filter(parent_asset_id=asset_id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_component(request, pk):
    """
    Lắp thêm linh kiện vào tài sản
    
    URL: /api/assets/<id>/upgrade/
    
    Input (JSON):
        {
            "component_id": 5,       // ID linh kiện cần lắp
            "notes": "Lắp RAM 16Gb"  // Ghi chú (optional)
        }
    
    Output:
        - 200: {
            "message": "Đã lắp linh kiện",
            "asset": {...},
            "component": {...}
        }
        - 400: Lỗi (component đang thuộc asset khác, không phải linh kiện)
        - 404: Không tìm thấy asset hoặc component
    
    Logic:
        1. Kiểm tra component tồn tại và category.is_component = true
        2. Kiểm tra component chưa thuộc asset nào (parent_asset = null)
        3. Cập nhật component.parent_asset = asset
        4. Ghi AssetHistory action=UPGRADE cho asset
        5. Trả về kết quả
    """
    # TODO: Implement
    component_id = request.data.get('component_id')
    notes = request.data.get('notes', '')
    
    try:
        asset = Asset.active_objects.get(pk=pk)
        component = Asset.active_objects.get(pk=component_id)
        
        # Validate
        if not component.category or not component.category.is_component:
            return Response(
                {"error": "Tài sản được chọn không phải là linh kiện"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if component.parent_asset is not None:
            return Response(
                {"error": f"Linh kiện đang thuộc về {component.parent_asset.asset_code}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update
        component.parent_asset = asset
        component.save()
        
        # Log history
        AssetHistory.objects.create(
            asset=asset,
            action=AssetAction.UPGRADE,
            note=f"Lắp thêm {component.name} ({component.asset_code}). {notes}".strip()
        )
        
        return Response({
            "message": "Đã lắp linh kiện thành công",
            "asset": AssetSerializer(asset).data,
            "component": AssetSerializer(component).data
        })
        
    except Asset.DoesNotExist:
        return Response(
            {"error": "Không tìm thấy tài sản"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retrieve_component(request, pk):
    """
    Tháo linh kiện khỏi tài sản
    
    URL: /api/assets/<id>/retrieve/
    
    Input (JSON):
        {
            "component_id": 5,           // ID linh kiện cần tháo
            "notes": "Tháo RAM cũ",       // Ghi chú (optional)
            "new_parent_id": 10          // Lắp vào asset khác (optional)
        }
    
    Output:
        - 200: {
            "message": "Đã tháo linh kiện",
            "asset": {...},
            "component": {...}
        }
        - 400: Lỗi (component không thuộc asset này)
        - 404: Không tìm thấy
    
    Logic:
        1. Kiểm tra component.parent_asset == asset
        2. Cập nhật component.parent_asset = new_parent hoặc null
        3. Ghi AssetHistory action=RETRIEVE cho asset gốc
        4. Nếu có new_parent, ghi action=UPGRADE cho asset mới
    """
    # TODO: Implement
    component_id = request.data.get('component_id')
    notes = request.data.get('notes', '')
    new_parent_id = request.data.get('new_parent_id')
    
    try:
        asset = Asset.active_objects.get(pk=pk)
        component = Asset.active_objects.get(pk=component_id)
        
        if component.parent_asset != asset:
            return Response(
                {"error": "Linh kiện không thuộc về tài sản này"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tháo ra
        component.parent_asset = None
        
        # Log history cho asset gốc
        AssetHistory.objects.create(
            asset=asset,
            action=AssetAction.RETRIEVE,
            note=f"Tháo {component.name} ({component.asset_code}). {notes}".strip()
        )
        
        # Nếu lắp vào asset mới
        if new_parent_id:
            new_parent = Asset.active_objects.get(pk=new_parent_id)
            component.parent_asset = new_parent
            
            AssetHistory.objects.create(
                asset=new_parent,
                action=AssetAction.UPGRADE,
                note=f"Lắp {component.name} từ {asset.asset_code}. {notes}".strip()
            )
        
        component.save()
        
        return Response({
            "message": "Đã tháo linh kiện",
            "asset": AssetSerializer(asset).data,
            "component": AssetSerializer(component).data
        })
        
    except Asset.DoesNotExist:
        return Response(
            {"error": "Không tìm thấy tài sản"},
            status=status.HTTP_404_NOT_FOUND
        )


# Export
__all__ = [
    'AssetComponentListView',
    'upgrade_component',
    'retrieve_component',
]
