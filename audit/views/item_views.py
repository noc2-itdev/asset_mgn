"""
AuditItem Views - Chi tiết kiểm kê từng tài sản
================================================

Người phụ trách: [Dev C2]
Nhánh Git: feature/audit-item

API Endpoints:
- GET    /api/audit-sessions/<session_id>/items/    → AuditItemListView
- POST   /api/audit-sessions/<session_id>/add-items/ → add_items_manual
- DELETE /api/audit-sessions/<session_id>/remove-items/ → remove_items
- GET    /api/audit-items/<id>/                     → AuditItemDetailView
- POST   /api/audit-items/<id>/check/               → check_item
- POST   /api/audit-items/<id>/mark-missing/        → mark_missing
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import AuditSession, AuditItem, AuditResultStatus
from ..serializers import AuditItemSerializer, AuditItemCheckSerializer


class AuditItemListView(generics.ListAPIView):
    """
    GET: Danh sách tài sản cần kiểm kê trong 1 session
    
    URL: /api/audit-sessions/<session_id>/items/
    
    Query params:
        - status: Lọc theo result_status (pending, matched, missing, ...)
        - page: Phân trang
    
    Response:
        - 200: Danh sách AuditItem với thông tin asset
    """
    serializer_class = AuditItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        queryset = AuditItem.objects.filter(audit_session_id=session_id)
        
        # TODO: Filter by result_status
        result_status = self.request.query_params.get('status')
        if result_status:
            queryset = queryset.filter(result_status=result_status)
        
        return queryset.select_related('asset', 'expected_location', 'actual_location')


class AuditItemDetailView(generics.RetrieveAPIView):
    """
    GET: Chi tiết một item kiểm kê
    
    Response:
        - 200: AuditItem với thông tin expected và actual
        - 404: Không tìm thấy
    """
    queryset = AuditItem.objects.all()
    serializer_class = AuditItemSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_items_manual(request, session_id):
    """
    Thêm tài sản thủ công vào danh sách kiểm kê
    
    Input (JSON):
        {
            "asset_ids": [1, 2, 3]  // Danh sách ID tài sản
        }
    
    Output:
        - 201: {"message": "Đã thêm X items", "count": X}
        - 400: Lỗi (session không phải draft/planned, asset đã có trong list)
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra session.status in [draft, planned]
        2. Lọc các asset chưa có trong session
        3. Gọi session.add_items_manual(asset_ids)
        4. Trả về số lượng đã thêm
    """
    # TODO: Implement
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_items(request, session_id):
    """
    Xóa tài sản khỏi danh sách kiểm kê
    
    Input (JSON):
        {
            "item_ids": [1, 2, 3]  // Danh sách ID AuditItem
        }
    
    Output:
        - 200: {"message": "Đã xóa X items", "count": X}
        - 400: Lỗi (session không phải draft/planned)
        - 404: Không tìm thấy session
    
    Logic:
        1. Kiểm tra session.status in [draft, planned]
        2. Xóa các items theo ID
        3. Cập nhật thống kê session
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_item(request, pk):
    """
    Ghi nhận kết quả kiểm kê cho 1 tài sản
    
    Input (JSON):
        {
            "actual_location_id": 5,        // ID vị trí thực tế (optional)
            "actual_status": "in_use",      // Trạng thái thực tế
            "actual_person_id": 3,          // ID người quản lý thực tế (optional)
            "notes": "Ghi chú",             // Ghi chú (optional)
            "photo": "base64...",           // Ảnh chụp (optional)
            "scanned_code": "QR123"         // Mã QR/Barcode đã quét (optional)
        }
    
    Output:
        - 200: {
            "item": {...},
            "result_status": "matched|location_mismatch|...",
            "discrepancies": ["Sai vị trí: A → B", ...]
        }
        - 400: Lỗi validation
        - 404: Không tìm thấy item
    
    Logic:
        1. Gọi item.check_asset(**data)
        2. Tự động xác định result_status dựa trên so sánh expected vs actual
        3. Cập nhật checked_at, checked_by
        4. Cập nhật thống kê session
    """
    # TODO: Implement
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_missing(request, pk):
    """
    Đánh dấu tài sản không tìm thấy
    
    Input (JSON):
        {
            "notes": "Lý do không tìm thấy"  // Optional
        }
    
    Output:
        - 200: {"item": {...}, "result_status": "missing"}
        - 400: Lỗi (item đã được kiểm)
        - 404: Không tìm thấy item
    
    Logic:
        1. Gọi item.mark_as_missing(notes, checked_by)
        2. Cập nhật thống kê session
    """
    # TODO: Implement
    pass


# Export tất cả
__all__ = [
    'AuditItemListView',
    'AuditItemDetailView',
    'add_items_manual',
    'remove_items',
    'check_item',
    'mark_missing',
]
