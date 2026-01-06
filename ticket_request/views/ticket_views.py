"""
TicketRequest Views - Yêu cầu sửa chữa/bảo trì
==============================================

Người phụ trách: [Dev D1]
Nhánh Git: feature/ticket-crud

API Endpoints:
- GET/POST  /api/tickets/            → TicketListView
- GET/PUT   /api/tickets/<id>/       → TicketDetailView
- POST      /api/tickets/<id>/approve/  → approve_ticket
- POST      /api/tickets/<id>/reject/   → reject_ticket
- POST      /api/tickets/<id>/complete/ → complete_ticket
"""

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main.models import TicketRequest
from ..serializers import TicketRequestSerializer


class TicketListView(generics.ListCreateAPIView):
    """
    GET: Danh sách yêu cầu
    POST: Tạo yêu cầu mới
    
    Query params:
        - status: pending, approved, rejected, completed
        - request_type: repair, maintenance, borrow, ...
        - asset_id: Lọc theo tài sản
    """
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Implement get_queryset and perform_create


class TicketDetailView(generics.RetrieveUpdateAPIView):
    """GET/PUT: Chi tiết & cập nhật (chỉ khi pending)"""
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer
    permission_classes = [IsAuthenticated]
    
    # TODO: Validate status before update


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_ticket(request, pk):
    """
    Duyệt yêu cầu
    
    Input: {"notes": "..."}
    Output: {"message": "Đã duyệt", "ticket": {...}}
    
    Logic:
        - Set status=approved, approved_by, approved_at
        - If request_type=repair: Asset.status = UNDER_REPAIR
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_ticket(request, pk):
    """
    Từ chối yêu cầu
    
    Input: {"reason": "Lý do"}
    Output: {"message": "Đã từ chối", "ticket": {...}}
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_ticket(request, pk):
    """
    Hoàn thành yêu cầu
    
    Input: {"resolution": "...", "new_asset_status": "in_use"}
    Output: {"message": "Hoàn thành", "ticket": {...}}
    
    Logic:
        - Set status=completed, completed_at
        - Update Asset.status if provided
    """
    # TODO: Implement
    raise NotImplementedError("Chức năng chưa được triển khai")


__all__ = [
    'TicketListView', 'TicketDetailView',
    'approve_ticket', 'reject_ticket', 'complete_ticket'
]
