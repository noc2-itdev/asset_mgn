"""
Ticket Request Views - Yêu cầu sửa chữa/bảo trì
================================================

Người phụ trách: [Dev D1]
Nhánh Git: feature/ticket-crud

API Endpoints:
- GET    /api/tickets/           → TicketListView
- POST   /api/tickets/           → TicketListView
- GET    /api/tickets/<id>/      → TicketDetailView
- PUT    /api/tickets/<id>/      → TicketDetailView
- POST   /api/tickets/<id>/approve/   → approve_ticket
- POST   /api/tickets/<id>/reject/    → reject_ticket
- POST   /api/tickets/<id>/complete/  → complete_ticket
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import TicketRequest, Asset, AssetHistory, AssetAction
from ..serializers import TicketRequestSerializer, TicketRequestDetailSerializer


class TicketListView(generics.ListCreateAPIView):
    """
    GET: Danh sách yêu cầu
    POST: Tạo yêu cầu mới
    
    Query params:
        - status: pending, approved, rejected, completed
        - request_type: repair, maintenance, borrow, return, other
        - asset_id: Lọc theo tài sản
    
    Response:
        - 200: Danh sách tickets
        - 201: Ticket mới
    """
    serializer_class = TicketRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = TicketRequest.objects.all()
        
        # Filter by status
        ticket_status = self.request.query_params.get('status')
        if ticket_status:
            queryset = queryset.filter(status=ticket_status)
        
        # Filter by request_type
        request_type = self.request.query_params.get('request_type')
        if request_type:
            queryset = queryset.filter(request_type=request_type)
        
        # Filter by asset
        asset_id = self.request.query_params.get('asset_id')
        if asset_id:
            queryset = queryset.filter(asset_id=asset_id)
        
        return queryset.select_related('asset', 'requester').order_by('-requested_at')
    
    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class TicketDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: Chi tiết yêu cầu
    PUT/PATCH: Cập nhật yêu cầu (chỉ khi status=pending)
    
    Response:
        - 200: Ticket detail
        - 400: Không thể sửa (status != pending)
    """
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            return Response(
                {"error": "Chỉ có thể sửa yêu cầu đang chờ duyệt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_ticket(request, pk):
    """
    Duyệt yêu cầu
    
    Input (JSON):
        {
            "notes": "Ghi chú khi duyệt"  // Optional
        }
    
    Output:
        - 200: {"message": "Đã duyệt", "ticket": {...}}
        - 400: Lỗi (status không phải pending)
    
    Logic:
        1. Kiểm tra status == pending
        2. Cập nhật status = approved, approved_by, approved_at
        3. Nếu request_type == repair, cập nhật Asset.status = UNDER_REPAIR
    """
    try:
        ticket = TicketRequest.objects.get(pk=pk)
        
        if ticket.status != 'pending':
            return Response(
                {"error": "Yêu cầu không ở trạng thái chờ duyệt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        ticket.status = 'approved'
        ticket.approved_by = request.user
        ticket.approved_at = timezone.now()
        ticket.save()
        
        # Nếu là yêu cầu sửa chữa, cập nhật trạng thái asset
        if ticket.request_type == 'repair' and ticket.asset:
            ticket.asset.status = 'under_repair'
            ticket.asset.save()
            
            AssetHistory.objects.create(
                asset=ticket.asset,
                action=AssetAction.STATUS_CHANGE,
                to_status='under_repair',
                related_ticket=ticket,
                note=f"Duyệt yêu cầu sửa chữa #{ticket.id}"
            )
        
        return Response({
            "message": "Đã duyệt yêu cầu",
            "ticket": TicketRequestDetailSerializer(ticket).data
        })
        
    except TicketRequest.DoesNotExist:
        return Response({"error": "Không tìm thấy yêu cầu"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_ticket(request, pk):
    """
    Từ chối yêu cầu
    
    Input (JSON):
        {
            "reason": "Lý do từ chối"  // Bắt buộc
        }
    
    Output:
        - 200: {"message": "Đã từ chối", "ticket": {...}}
        - 400: Lỗi
    """
    reason = request.data.get('reason', '')
    
    if not reason:
        return Response(
            {"error": "Vui lòng nhập lý do từ chối"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        ticket = TicketRequest.objects.get(pk=pk)
        
        if ticket.status != 'pending':
            return Response(
                {"error": "Yêu cầu không ở trạng thái chờ duyệt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        ticket.status = 'rejected'
        ticket.approved_by = request.user
        ticket.approved_at = timezone.now()
        ticket.note = f"{ticket.note}\n\nLý do từ chối: {reason}".strip()
        ticket.save()
        
        return Response({
            "message": "Đã từ chối yêu cầu",
            "ticket": TicketRequestDetailSerializer(ticket).data
        })
        
    except TicketRequest.DoesNotExist:
        return Response({"error": "Không tìm thấy yêu cầu"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_ticket(request, pk):
    """
    Hoàn thành yêu cầu
    
    Input (JSON):
        {
            "resolution": "Mô tả công việc đã thực hiện",
            "new_asset_status": "in_use"  // Trạng thái mới của asset (optional)
        }
    
    Output:
        - 200: {"message": "Đã hoàn thành", "ticket": {...}}
        - 400: Lỗi (status không phải approved)
    
    Logic:
        1. Kiểm tra status == approved
        2. Cập nhật status = completed, completed_at
        3. Cập nhật Asset.status nếu có
        4. Ghi AssetHistory
    """
    resolution = request.data.get('resolution', '')
    new_asset_status = request.data.get('new_asset_status')
    
    try:
        ticket = TicketRequest.objects.get(pk=pk)
        
        if ticket.status != 'approved':
            return Response(
                {"error": "Yêu cầu chưa được duyệt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        ticket.status = 'completed'
        ticket.completed_at = timezone.now()
        ticket.note = f"{ticket.note}\n\nKết quả: {resolution}".strip()
        ticket.save()
        
        # Cập nhật trạng thái asset
        if new_asset_status and ticket.asset:
            old_status = ticket.asset.status
            ticket.asset.status = new_asset_status
            ticket.asset.save()
            
            AssetHistory.objects.create(
                asset=ticket.asset,
                action=AssetAction.STATUS_CHANGE,
                from_status=old_status,
                to_status=new_asset_status,
                related_ticket=ticket,
                note=f"Hoàn thành yêu cầu #{ticket.id}"
            )
        
        return Response({
            "message": "Đã hoàn thành yêu cầu",
            "ticket": TicketRequestDetailSerializer(ticket).data
        })
        
    except TicketRequest.DoesNotExist:
        return Response({"error": "Không tìm thấy yêu cầu"}, status=status.HTTP_404_NOT_FOUND)


# Export
__all__ = [
    'TicketListView',
    'TicketDetailView',
    'approve_ticket',
    'reject_ticket',
    'complete_ticket',
]
