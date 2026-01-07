"""
Asset Views - CRUD và quản lý tài sản
=====================================

Người phụ trách: [Dev B1]
Nhánh Git: feature/asset-crud

API Endpoints:
- GET/POST  /api/assets/              → AssetListView
- GET/PUT   /api/assets/<id>/         → AssetDetailView
- GET       /api/assets/qr/<code>/    → qr_lookup
- POST      /api/assets/<id>/split/   → split_asset (MỚI)
- GET       /api/assets/<id>/history/ → AssetHistoryListView
"""

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Asset, AssetHistory
from ..serializers import AssetSerializer, AssetDetailSerializer, AssetHistorySerializer


class AssetListView(generics.ListCreateAPIView):
    """
    GET: Danh sách tài sản
    POST: Tạo tài sản mới
    
    Query params:
        - status: in_use, in_storage, broken, ...
        - category, department, location: Filter by ID
        - search: Tìm theo name, asset_code, serial_number
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset with filtering


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Chi tiết tài sản
    PUT/PATCH: Cập nhật
    DELETE: Soft delete
    """
    queryset = Asset.active_objects.all()
    serializer_class = AssetDetailSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Override destroy for soft delete


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_lookup(request, code):
    """
    Tra cứu tài sản theo QR/Barcode
    
    Output:
        - 200: Asset detail
        - 404: Không tìm thấy
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def split_asset(request, pk):
    """
    Tách lô tài sản thành bản ghi mới
    
    URL: /api/assets/<id>/split/
    
    Input (JSON):
        {
            "split_quantity": 5,           // Số lượng cần tách (bắt buộc)
            "reason": "Ghế hỏng",          // Lý do (optional)
            "new_status": "broken",        // Trạng thái mới (optional)
            "new_asset_code": "GH-001-1"   // Mã mới (optional, tự sinh nếu bỏ trống)
        }
    
    Output:
        - 200: {
            "message": "Đã tách thành công",
            "original_asset": {...},
            "new_asset": {...}
        }
        - 400: Lỗi (quantity >= current quantity)
    
    Logic:
        - Gọi Asset.split() method
        - Tự động ghi AssetHistory cho cả 2 bản ghi
    """
    # TODO: Implement using Asset.split() method
    raise NotImplementedError("Chức năng chưa được triển khai")


class AssetHistoryListView(generics.ListAPIView):
    """
    GET: Lịch sử biến động của tài sản
    
    Query params:
        - action: Lọc theo loại hành động
        - from_date, to_date: Lọc theo thời gian
    """
    serializer_class = AssetHistorySerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset


__all__ = ['AssetListView', 'AssetDetailView', 'qr_lookup', 'split_asset', 'AssetHistoryListView']
