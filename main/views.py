from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from .models import Department, Person, AssetCategory, Asset, AssetHistory, TicketRequest, AssetAudit, Location, \
    AssetAttachment, AssetStatus, AssetAction, TicketRequestStatus
from .serializers import (
    DepartmentSerializer, PersonSerializer, AssetCategorySerializer, LocationSerializer, AssetAttachmentSerializer,
    AssetSerializer, AssetCreateUpdateSerializer, AssetHistorySerializer,
    TicketRequestSerializer, AssetAuditSerializer
)


# @Todo: Class-based View (CBV) hoạt động không theo tuần tự, sử dụng cơ chế kế thừa (ListCreateAPIView) và khai báo thuộc tính (permission_classes, queryset, serializer_class) để DRF tự động xử lý
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


# @Todo: Function-based View (FBV) được gọi là lập trình hướng thủ tục (viết từng bước logic xử lý theo tuần tự), cần định nghĩa rõ ràng logic xử lý cho từng phương thức HTTP (GET, POST)
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def department_list_create_fbv(request):
#     """
#     Xử lý hành động LIST (GET) và CREATE (POST) cho đối tượng Department.
#     Chỉ cho phép người dùng đã xác thực truy cập.
#     """
#
#     # --- LIST LOGIC (GET request) ---
#     if request.method == 'GET':
#         # 1. Truy cập Queryset: Lấy tất cả các đối tượng (matching queryset = Department.objects.all())
#         departments = Department.objects.all()
#
#         # 2. Serialize dữ liệu: Chuyển đổi từ Python sang định dạng Response (matching serializer_class)
#         serializer = DepartmentSerializer(departments, many=True)
#
#         # 3. Trả về Response
#         return Response(serializer.data)
#
#     # --- CREATE LOGIC (POST request) ---
#     elif request.method == 'POST':
#         # 1. Deserialize/Validate dữ liệu: Khởi tạo Serializer với dữ liệu gửi đến
#         serializer = DepartmentSerializer(data=request.data)
#
#         # 2. Xác thực dữ liệu
#         if serializer.is_valid():
#             # 3. Lưu đối tượng mới (Tương đương với logic .save() trong ListCreateAPIView)
#             serializer.save()
#
#             # 4. Trả về phản hồi thành công (HTTP 201 Created)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         # 5. Trả về lỗi nếu dữ liệu không hợp lệ
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class AssetCategoryListCreateView(generics.ListCreateAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetAttachmentListCreateView(generics.ListCreateAPIView):
    queryset = AssetAttachment.objects.all()
    serializer_class = AssetAttachmentSerializer
    permission_classes = [IsAuthenticated]


class AssetAttachmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetAttachment.objects.all()
    serializer_class = AssetAttachmentSerializer
    permission_classes = [IsAuthenticated]


class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    # Tùy chỉnh Queryset: Cách đơn giản nhất để lọc queryset của bất kỳ view nào kế thừa từ GenericAPIView là ghi đè phương thức .get_queryset()
    # Trong lập trình hướng đối tượng (OOP), khi bạn muốn thay đổi hành vi của một phương thức đã được định nghĩa trong lớp cha (như GenericAPIView),
    # bạn phải ghi đè (override) phương thức đó bằng cách sử dụng tên chính xác của nó
    # Nhờ có self mà có thể truy cập vào đối tượng request của DRF thông qua self.request.
    # Đối tượng request này là thành phần quan trọng nhất vì nó chứa thông tin về yêu cầu HTTP hiện tại (người dùng, phương thức, dữ liệu, tham số truy vấn, v.v.).
    def get_queryset(self):
        queryset = Asset.objects.all()
        # Lọc theo danh mục
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)

        # Lọc theo trạng thái
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)

        # Lọc theo phòng ban
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(current_department__id=department)

        # Tìm kiếm theo tên hoặc mã tài sản
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(asset_code__icontains=search)
            )

        # Tìm kiếm theo vị trí đặt tài sản
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__id=location)

        # Lọc theo tài sản độc lập (đối soát kế toán)
        has_independent_value = self.request.query_params.get('has_independent_value', None)
        if has_independent_value is not None:
            queryset = queryset.filter(has_independent_value=has_independent_value.lower() == 'true')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssetCreateUpdateSerializer
        return AssetSerializer


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AssetCreateUpdateSerializer
        return AssetSerializer


class AssetComponentsView(generics.ListAPIView):
    """Liệt kê tất cả linh kiện của một tài sản"""
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        asset_id = self.kwargs['pk']
        return Asset.objects.filter(parent_asset__id=asset_id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_asset(request, pk):
    """
    Bàn giao tài sản cho cá nhân/phòng ban khác
    """
    asset = get_object_or_404(Asset, pk=pk)

    to_department_id = request.data.get('to_department')
    to_person_id = request.data.get('to_person')
    note = request.data.get('note', '')

    if not to_department_id and not to_person_id:
        return Response(
            {'error': 'Cần chỉ định ít nhất một trong: to_department hoặc to_person'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        # Lưu thông tin trước khi thay đổi
        old_department = asset.current_department
        old_person = asset.current_person

        # Cập nhật tài sản
        if to_department_id:
            asset.current_department = Department.objects.get(pk=to_department_id)
        if to_person_id:
            asset.current_person = Person.objects.get(pk=to_person_id)
        asset.save()

        # Tạo lịch sử
        AssetHistory.objects.create(
            asset=asset,
            action=AssetAction.TRANSFER,
            from_department=old_department,
            to_department=asset.current_department,
            from_person=old_person,
            to_person=asset.current_person,
            note=note
        )

    return Response({'message': 'Bàn giao tài sản thành công'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_component(request, pk):
    """
    Nâng cấp linh kiện của tài sản (thêm/xóa/thay thế linh kiện)
    """
    parent_asset = get_object_or_404(Asset, pk=pk)

    component_id = request.data.get('component_id')
    action = request.data.get('action')  # add, remove, replace
    new_component_data = request.data.get('new_component', {})
    note = request.data.get('note', '')

    if action not in ['add', 'remove', 'replace']:
        return Response(
            {'error': 'Hành động không hợp lệ. Chọn một trong: add, remove, replace'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        if action == 'add':
            # Thêm linh kiện mới
            new_component_data['parent_asset'] = parent_asset
            new_component_data['category'] = new_component_data.get('category')
            new_component = Asset.objects.create(**new_component_data)

            # Ghi lịch sử
            AssetHistory.objects.create(
                asset=new_component,
                action=AssetAction.UPGRADE,
                to_department=parent_asset.current_department,
                to_person=parent_asset.current_person,
                note=f'Thêm linh kiện cho {parent_asset.name}. {note}'
            )

        elif action == 'remove':
            # Xóa linh kiện
            component = get_object_or_404(Asset, pk=component_id, parent_asset=parent_asset)
            component.delete()

            # Ghi lịch sử
            AssetHistory.objects.create(
                asset=parent_asset,
                action=AssetAction.UPGRADE,
                from_department=parent_asset.current_department,
                from_person=parent_asset.current_person,
                note=f'Xóa linh kiện {component.name}. {note}'
            )

        elif action == 'replace':
            # Thay thế linh kiện
            old_component = get_object_or_404(Asset, pk=component_id, parent_asset=parent_asset)
            old_component_data = {
                'name': old_component.name,
                'category': old_component.category,
                'asset_code': old_component.asset_code,
                'status': old_component.status,
                'current_department': old_component.current_department,
                'current_person': old_component.current_person,
            }

            # Xóa linh kiện cũ
            old_component.delete()

            # Tạo linh kiện mới
            new_component_data.update({
                'parent_asset': parent_asset,
                'asset_code': new_component_data.get('asset_code', old_component_data['asset_code'])
            })
            new_component = Asset.objects.create(**new_component_data)

            # Ghi lịch sử
            AssetHistory.objects.create(
                asset=parent_asset,
                action=AssetAction.UPGRADE,
                note=f'Thay thế linh kiện {old_component_data["name"]} bằng {new_component.name}. {note}'
            )

    return Response({'message': 'Nâng cấp linh kiện thành công'}, status=status.HTTP_200_OK)


class AssetHistoryListView(generics.ListAPIView):
    """Liệt kê lịch sử của một tài sản"""
    serializer_class = AssetHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        asset_id = self.kwargs['pk']
        return AssetHistory.objects.filter(asset__id=asset_id).order_by('-date')


class TicketRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TicketRequest.objects.all()
        asset_id = self.request.query_params.get('asset', None)
        status_param = self.request.query_params.get('status', None)
        request_type = self.request.query_params.get('request_type', None)

        if asset_id:
            queryset = queryset.filter(asset__id=asset_id)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if request_type:
            queryset = queryset.filter(request_type=request_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class TicketRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        status_update = request.data.get('status')
        resolution_note = request.data.get('resolution_note', '')

        if status_update:
            instance.status = status_update
        if resolution_note:
            instance.resolution_note = resolution_note

        if status_update or resolution_note:
            instance.handler = request.user
            instance.save()

            # Nếu yêu cầu được hoàn thành, ghi lịch sử
            if status_update == TicketRequestStatus.COMPLETED:
                AssetHistory.objects.create(
                    asset=instance.asset,
                    action=AssetAction.REPAIR,  # Có thể cần cập nhật action tùy theo loại request
                    note=f'Hoàn thành yêu cầu: {resolution_note}'
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AssetAuditListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetAuditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AssetAudit.objects.all()
        asset_id = self.request.query_params.get('asset', None)

        if asset_id:
            queryset = queryset.filter(asset__id=asset_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(auditor=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asset_statistics(request):
    """
    Thống kê tài sản theo trạng thái, danh mục tài sản
    """
    # Tổng số tài sản độc lập (cần đối soát kế toán)
    independent_assets_count = Asset.objects.filter(has_independent_value=True).count()

    total_assets = Asset.objects.count()
    by_status = {}
    for status_choice in AssetStatus.choices:
        count = Asset.objects.filter(status=status_choice[0]).count()
        by_status[status_choice[1]] = count

    by_category = {}
    categories = AssetCategory.objects.all()
    for category in categories:
        count = Asset.objects.filter(category=category).count()
        by_category[category.name] = count

    data = {
        'total_assets': total_assets,
        'independent_assets': independent_assets_count,
        'by_status': by_status,
        'by_category': by_category
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_locations(request):
    """
    Lấy danh sách tất cả các vị trí duy nhất
    """
    locations = Asset.objects.values_list('location__name', flat=True).distinct().order_by('location__name')
    return Response([loc for loc in locations if loc])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asset_qr_lookup(request, asset_code):
   """
   Tìm kiếm tài sản theo mã QR code
   """
   try:
       asset = Asset.objects.get(asset_code=asset_code)
       serializer = AssetSerializer(asset)
       return Response(serializer.data)
   except Asset.DoesNotExist:
       return Response(
           {'error': 'Không tìm thấy tài sản với mã QR này'},
           status=status.HTTP_404_NOT_FOUND
       )