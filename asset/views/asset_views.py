"""
Asset Views - CRUD và quản lý tài sản
=====================================

Người phụ trách: [Dev B1]
Nhánh Git: feature/asset-crud

API Endpoints:
- GET    /api/assets/              → AssetListView
- POST   /api/assets/              → AssetListView  
- GET    /api/assets/<id>/         → AssetDetailView
- PUT    /api/assets/<id>/         → AssetDetailView
- DELETE /api/assets/<id>/         → AssetDetailView (soft delete)
- GET    /api/assets/qr/<code>/    → qr_lookup
- GET    /api/assets/<id>/history/ → AssetHistoryListView
"""

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from main.models import Asset, AssetHistory
from ..serializers import AssetSerializer, AssetDetailSerializer, AssetHistorySerializer


class AssetListView(generics.ListCreateAPIView):
    """
    GET: Danh sách tài sản
    POST: Tạo tài sản mới
    
    Query params:
        - status: Lọc theo trạng thái (in_use, in_storage, broken, ...)
        - category: Lọc theo loại tài sản (ID)
        - department: Lọc theo phòng ban (ID)
        - location: Lọc theo vị trí (ID)
        - search: Tìm kiếm theo name, asset_code, serial_number
        - is_component: true/false - Lọc linh kiện
    
    Response:
        - 200: Danh sách Asset (phân trang)
        - 201: Asset mới được tạo
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'current_department', 'location']
    search_fields = ['name', 'asset_code', 'serial_number']
    ordering_fields = ['name', 'asset_code', 'created_at']
    ordering = ['-id']
    
    def get_queryset(self):
        # Chỉ lấy tài sản chưa xóa
        queryset = Asset.active_objects.all()
        
        # TODO: Filter is_component
        is_component = self.request.query_params.get('is_component')
        if is_component is not None:
            # Filter based on category.is_component
            pass
        
        return queryset.select_related(
            'category', 'current_department', 'current_person', 'location'
        )


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Chi tiết tài sản
    PUT/PATCH: Cập nhật thông tin tài sản
    DELETE: Soft delete tài sản
    
    Response:
        - 200: Asset detail với components và attachments
        - 404: Không tìm thấy
    """
    queryset = Asset.active_objects.all()
    serializer_class = AssetDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete - không xóa thật"""
        instance = self.get_object()
        instance.delete()  # Gọi soft delete method
        return Response(
            {"message": f"Đã xóa tài sản {instance.asset_code}"},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_lookup(request, code):
    """
    Tra cứu tài sản theo mã QR/Barcode
    
    URL: /api/assets/qr/<code>/
    
    Input:
        - code: Mã QR hoặc asset_code
    
    Output:
        - 200: Asset detail
        - 404: Không tìm thấy tài sản với mã này
    
    Logic:
        1. Tìm Asset theo asset_code
        2. Trả về thông tin chi tiết
    """
    try:
        asset = Asset.active_objects.get(asset_code=code)
        serializer = AssetDetailSerializer(asset)
        return Response(serializer.data)
    except Asset.DoesNotExist:
        return Response(
            {"error": f"Không tìm thấy tài sản với mã: {code}"},
            status=status.HTTP_404_NOT_FOUND
        )


class AssetHistoryListView(generics.ListAPIView):
    """
    GET: Lịch sử biến động của tài sản
    
    URL: /api/assets/<id>/history/
    
    Query params:
        - action: Lọc theo loại hành động
        - from_date, to_date: Lọc theo khoảng thời gian
    
    Response:
        - 200: Danh sách AssetHistory
    """
    serializer_class = AssetHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        asset_id = self.kwargs.get('pk')
        queryset = AssetHistory.objects.filter(asset_id=asset_id)
        
        # TODO: Filter by action, date range
        
        return queryset.order_by('-date')


# Export
__all__ = [
    'AssetListView',
    'AssetDetailView',
    'qr_lookup',
    'AssetHistoryListView',
]
