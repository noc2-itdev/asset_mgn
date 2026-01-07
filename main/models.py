import qrcode
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
from django.utils import timezone


# Department: Đơn vị quản lý tài sản.
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Person: Cá nhân chịu trách nhiệm tài sản.
class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# Location: Địa điểm lắp đặt tài sản. Dùng cho nhu cầu kiểm kê theo vị trí lắp đặt bên cạnh theo Department
class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# AssetStatus: Trạng thái tài sản (đang sử dụng, lưu kho, thanh lý, ...).
class AssetStatus(models.TextChoices):
    IN_USE = 'in_use', 'Đang sử dụng'
    IN_STORAGE = 'in_storage', 'Lưu kho'
    LIQUIDATED = 'liquidated', 'Thanh lý'
    BROKEN = 'broken', 'Hư hỏng'


# AssetCategory: phân loại linh kiện và tài sản chính. (máy tính, máy in, RAM, SSD,...).
class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_component = models.BooleanField(
        default=False, 
        help_text="Đánh dấu nếu đây là linh kiện có thể tách rời khỏi thiết bị (RAM, SSD, Card màn hình)"
    )  # True cho RAM, SSD; False cho Máy tính
    def __str__(self):
        return self.name


# Tài sản: máy tính, máy in,...
class Asset(models.Model):
    # === THÔNG TIN CƠ BẢN ===
    name = models.CharField(max_length=255, help_text="Tên tài sản")
    category = models.ForeignKey('AssetCategory', on_delete=models.SET_NULL, null=True)
    parent_asset = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='components',
        help_text="Tài sản cấp trên (VD: RAM thuộc Máy tính nào)"
    )
    asset_code = models.CharField(max_length=100, unique=True, help_text="Mã tài sản")
    internal_code = models.CharField(max_length=50, blank=True, help_text="Ký hiệu nội bộ")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    status = models.CharField(max_length=20, choices=AssetStatus.choices, default=AssetStatus.IN_STORAGE)
    
    # === THÔNG TIN ĐỊNH LƯỢNG ===
    unit = models.CharField(
        max_length=20,
        default='cái',
        choices=[
            ('cái', 'Cái'),
            ('bộ', 'Bộ'),
            ('chiếc', 'Chiếc'),
            ('máy', 'Máy'),
            ('thanh', 'Thanh'),
            ('hộp', 'Hộp'),
        ],
        help_text="Đơn vị tính"
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Số lượng")
    
    # === THÔNG TIN VỊ TRÍ & QUẢN LÝ ===
    current_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    current_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, help_text="Vị trí hiện tại")
    
    # === THÔNG TIN KỸ THUẬT ===
    serial_number = models.CharField(max_length=100, blank=True, help_text="Số serial")
    model = models.CharField(max_length=100, blank=True, help_text="Model thiết bị")
    part_number = models.CharField(max_length=100, blank=True, help_text="Mã linh kiện (Part Number)")
    vendor = models.CharField(max_length=255, blank=True, help_text="Nhà cung cấp/Nhãn hiệu")
    country_of_origin = models.CharField(max_length=50, blank=True, help_text="Nước sản xuất")
    manufacturing_year = models.PositiveIntegerField(null=True, blank=True, help_text="Năm sản xuất")
    
    # === THÔNG TIN MUA SẮM & TIẾP NHẬN ===
    acquisition_type = models.CharField(
        max_length=50,
        choices=[
            ('purchase', 'Mua sắm'),
            ('transfer', 'Điều chuyển nội bộ'),
            ('donation', 'Tiếp nhận/Tặng'),
            ('grant', 'Cấp phát'),
            ('project', 'Dự án đầu tư'),
        ],
        default='purchase',
        help_text="Hình thức tiếp nhận"
    )
    acquisition_date = models.DateField(null=True, blank=True, help_text="Ngày đưa vào sử dụng")
    purchase_date = models.DateField(null=True, blank=True, help_text="Ngày mua sắm")
    warranty_expiry = models.DateField(null=True, blank=True, help_text="Hạn bảo hành")
    
    # === THÔNG TIN KẾ TOÁN & KHẤU HAO ===
    accounting_code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        unique=True,
        help_text="Số hiệu tài sản kế toán"
    )
    original_value = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Nguyên giá (VNĐ)"
    )
    depreciation_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Tỷ lệ khấu hao (%/năm)"
    )
    useful_life_years = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Số năm sử dụng (thời gian khấu hao)"
    )
    has_independent_value = models.BooleanField(
        default=True,
        help_text="Có giá trị độc lập cần đối soát kế toán"
    )
    
    # === GHI CHÚ & SOFT DELETE ===
    note = models.TextField(blank=True, help_text="Ghi chú")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # === PROPERTIES TÍNH TOÁN ===
    @property
    def residual_value(self):
        """Tính giá trị còn lại sau khấu hao"""
        if not self.original_value or not self.depreciation_rate or not self.acquisition_date:
            return self.original_value
        
        from datetime import date
        years_used = (date.today() - self.acquisition_date).days / 365
        depreciation = self.original_value * (self.depreciation_rate / 100) * years_used
        residual = self.original_value - depreciation
        return max(residual, 0)

    @property
    def total_value(self):
        """Tính thành tiền (số lượng x nguyên giá)"""
        if self.original_value and self.quantity:
            return self.original_value * self.quantity
        return self.original_value

    def split(self, split_quantity, reason='', new_status=None, new_asset_code=None):
        """
        Tách một phần tài sản thành bản ghi mới.
        Dùng khi nhập theo lô và cần tách riêng (VD: 1 ghế hỏng trong 30 ghế).
        
        Args:
            split_quantity: Số lượng cần tách
            reason: Lý do tách
            new_status: Trạng thái mới cho phần tách (mặc định giữ nguyên)
            new_asset_code: Mã tài sản mới (mặc định tự sinh)
        
        Returns:
            Asset: Bản ghi mới được tách ra
        
        Raises:
            ValidationError: Nếu số lượng tách >= số lượng hiện có
        """
        if split_quantity >= self.quantity:
            raise ValidationError(f"Số lượng tách ({split_quantity}) phải nhỏ hơn số lượng hiện có ({self.quantity})")
        
        if split_quantity <= 0:
            raise ValidationError("Số lượng tách phải lớn hơn 0")
        
        # Giữ lại số lượng gốc để ghi log
        original_quantity = self.quantity
        
        # Giảm số lượng bản gốc
        self.quantity -= split_quantity
        self.save()
        
        # Sinh mã mới nếu không cung cấp
        if not new_asset_code:
            # Tìm suffix phù hợp
            suffix = 1
            while Asset.objects.filter(asset_code=f"{self.asset_code}-{suffix}").exists():
                suffix += 1
            new_asset_code = f"{self.asset_code}-{suffix}"
        
        # Tạo bản ghi mới với các thuộc tính copy từ bản gốc
        new_asset = Asset.objects.create(
            name=self.name,
            category=self.category,
            asset_code=new_asset_code,
            internal_code=self.internal_code,
            unit=self.unit,
            quantity=split_quantity,
            status=new_status or self.status,
            current_department=self.current_department,
            current_person=self.current_person,
            location=self.location,
            serial_number='',  # Serial riêng
            model=self.model,
            part_number=self.part_number,
            vendor=self.vendor,
            country_of_origin=self.country_of_origin,
            manufacturing_year=self.manufacturing_year,
            acquisition_type=self.acquisition_type,
            acquisition_date=self.acquisition_date,
            purchase_date=self.purchase_date,
            warranty_expiry=self.warranty_expiry,
            accounting_code=None,  # Mã kế toán riêng
            original_value=self.original_value,
            depreciation_rate=self.depreciation_rate,
            useful_life_years=self.useful_life_years,
            has_independent_value=self.has_independent_value,
            note=f"Tách từ {self.asset_code}. {reason}".strip(),
        )
        
        # Import model AssetHistory để ghi log
        from main.models import AssetHistory, AssetAction
        
        # Ghi lịch sử cho bản gốc
        AssetHistory.objects.create(
            asset=self,
            action=AssetAction.SPLIT,
            note=f"Tách {split_quantity} {self.unit} → {new_asset_code}. Còn lại: {self.quantity}/{original_quantity}. {reason}".strip()
        )
        
        # Ghi lịch sử cho bản mới
        AssetHistory.objects.create(
            asset=new_asset,
            action=AssetAction.CREATE,
            note=f"Được tách từ {self.asset_code} ({split_quantity}/{original_quantity} {self.unit}). {reason}".strip(),
            to_status=new_status or self.status,
        )
        
        return new_asset

    # === METHODS ===
    def delete(self):
        """Soft delete - chỉ đánh dấu đã xóa"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_deleted=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        indexes = [
            models.Index(fields=['asset_code']),
            models.Index(fields=['category']),
            models.Index(fields=['current_department']),
            models.Index(fields=['location']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        if self.parent_asset and self.parent_asset == self:
            raise ValidationError("Tài sản không thể thuộc về chính nó.")

    def save(self, *args, **kwargs):
        if not self.qr_code and self.asset_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.asset_code)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')

            self.qr_code.save(f'qr_{self.asset_code}.png', File(buffer), save=False)
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.asset_code})"

    @property
    def is_component(self):
        """Xác định tài sản có phải là component dựa trên danh mục"""
        return self.category.is_component if self.category else False



# AssetAttachment: Tài liệu đính kèm để 1 tài sản có thể lưu trữ nhiều file cùng lúc như hóa đơn mua sắm, giấy tờ thanh lý,...
class AssetAttachment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='asset_attachments/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.asset_code} - {self.file.name}"


class AssetAction(models.TextChoices):
    """Các loại hành động trên tài sản để ghi lịch sử"""
    # Tạo/Cập nhật
    CREATE = 'create', 'Tạo mới'
    UPDATE = 'update', 'Cập nhật thông tin'
    SPLIT = 'split', 'Tách tài sản'  # 👈 MỚI: Tách từ lô
    
    # Chuyển giao/Di chuyển
    TRANSFER = 'transfer', 'Bàn giao'
    LOCATION_CHANGE = 'location_change', 'Thay đổi vị trí'
    STATUS_CHANGE = 'status_change', 'Thay đổi trạng thái'
    
    # Mượn/Trả
    BORROW = 'borrow', 'Cho mượn'
    RETURN = 'return', 'Trả lại'  # 👈 MỚI: Trả tài sản mượn
    
    # Linh kiện
    UPGRADE = 'upgrade', 'Nâng cấp/Lắp thêm'  # Lắp linh kiện mới
    RETRIEVE = 'retrieve', 'Thu hồi/Tháo ra'  # Tháo linh kiện
    
    # Bảo trì/Sửa chữa
    REPAIR = 'repair', 'Sửa chữa'
    MAINTENANCE = 'maintenance', 'Bảo trì'
    
    # Kiểm kê
    AUDIT = 'audit', 'Kiểm kê'


# Lưu lịch sử thay đổi của tài sản (bàn giao, sửa chữa, di dời, ...).
class AssetHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='histories')
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=AssetAction.choices, default=AssetAction.TRANSFER)
    from_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='from_histories')
    to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='to_histories')
    from_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='from_person_histories')
    to_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='to_person_histories')
    note = models.TextField(blank=True)
    from_status = models.CharField(max_length=20, choices=AssetStatus.choices, null=True, blank=True)
    to_status = models.CharField(max_length=20, choices=AssetStatus.choices, null=True, blank=True)
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='from_histories')
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='to_histories')
    related_ticket = models.ForeignKey('TicketRequest', on_delete=models.SET_NULL, null=True, blank=True)
    related_audit = models.ForeignKey('AuditItem', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.asset} - {self.action} - {self.date}"


class TicketRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Chờ xử lý'
    IN_PROGRESS = 'in_progress', 'Đang xử lý'
    COMPLETED = 'completed', 'Hoàn thành'
    REJECTED = 'rejected', 'Từ chối'


# TicketRequest: Quản lý yêu cầu sửa chữa/bảo trì từ tài sản thuộc bản thân quản lý hoặc yêu cầu mượn tài sản từ kho
class TicketRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('repair', 'Sửa chữa'),
        ('borrow', 'Mượn tài sản'),
        ('maintenance', 'Bảo trì'),
    ]

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='repair')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TicketRequestStatus.choices, default=TicketRequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_tickets')
    resolution_note = models.TextField(blank=True)
    # Các trường dùng cho bảo trì định kỳ
    scheduled_date = models.DateField(null=True, blank=True, help_text="Ngày dự kiến thực hiện")
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Hàng tháng'),
            ('quarterly', 'Hàng quý'),
            ('semi_annual', '6 tháng'),
            ('annual', 'Hàng năm'),
        ],
        null=True,
        blank=True,
        help_text="Tần suất bảo trì"
    )
    is_recurring = models.BooleanField(default=False, help_text="Là yêu cầu bảo trì định kỳ")  # True: Hệ thống có thể lên lịch tự động tạo ticket bảo trì cho các tài sản cần bảo trì định kỳ
    next_maintenance_date = models.DateField(null=True, blank=True, help_text="Ngày bảo trì tiếp theo")

    def __str__(self):
        return f"Yêu cầu {self.request_type}: {self.asset} - {self.get_status_display()}"


# ============================================================================
# KIỂM KÊ TÀI SẢN (AUDIT) - FR4.1, FR4.2, FR4.3
# ============================================================================

class AuditSessionStatus(models.TextChoices):
    """Trạng thái đợt kiểm kê"""
    DRAFT = 'draft', 'Bản nháp'
    PLANNED = 'planned', 'Đã lên kế hoạch'
    IN_PROGRESS = 'in_progress', 'Đang thực hiện'
    COMPLETED = 'completed', 'Hoàn thành'
    CANCELLED = 'cancelled', 'Đã hủy'


class AuditScope(models.TextChoices):
    """Phạm vi kiểm kê"""
    FULL = 'full', 'Toàn bộ tài sản'
    DEPARTMENT = 'department', 'Theo phòng ban'
    LOCATION = 'location', 'Theo vị trí'
    CATEGORY = 'category', 'Theo loại tài sản'
    CUSTOM = 'custom', 'Tùy chọn (chọn thủ công)'


class AuditResultStatus(models.TextChoices):
    """Kết quả kiểm kê từng tài sản"""
    PENDING = 'pending', 'Chưa kiểm kê'
    MATCHED = 'matched', 'Khớp'
    LOCATION_MISMATCH = 'location_mismatch', 'Sai vị trí'
    STATUS_MISMATCH = 'status_mismatch', 'Sai trạng thái'
    PERSON_MISMATCH = 'person_mismatch', 'Sai người quản lý'
    MISSING = 'missing', 'Không tìm thấy'
    DAMAGED = 'damaged', 'Hư hỏng phát hiện'
    EXCESS = 'excess', 'Thừa (không có trong hệ thống)'


class AuditActionType(models.TextChoices):
    """Loại đề xuất xử lý chênh lệch"""
    UPDATE_LOCATION = 'update_location', 'Cập nhật vị trí'
    UPDATE_STATUS = 'update_status', 'Cập nhật trạng thái'
    UPDATE_PERSON = 'update_person', 'Cập nhật người quản lý'
    REPORT_MISSING = 'report_missing', 'Báo mất'
    REPAIR = 'repair', 'Sửa chữa'
    LIQUIDATE = 'liquidate', 'Thanh lý'
    COMPENSATE = 'compensate', 'Yêu cầu bồi thường'
    CREATE_NEW = 'create_new', 'Tạo mới (tài sản thừa)'
    NO_ACTION = 'no_action', 'Không cần xử lý'


class AuditActionStatus(models.TextChoices):
    """Trạng thái đề xuất xử lý"""
    PROPOSED = 'proposed', 'Đề xuất'
    APPROVED = 'approved', 'Đã duyệt'
    REJECTED = 'rejected', 'Từ chối'
    EXECUTED = 'executed', 'Đã thực hiện'


class AuditSession(models.Model):
    """
    Đợt kiểm kê - FR4.1: Lập kế hoạch kiểm kê
    Quản lý thông tin về một đợt/kỳ kiểm kê tài sản
    """
    # Thông tin cơ bản
    code = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Mã đợt kiểm kê (VD: KK-2026-Q1)"
    )
    name = models.CharField(max_length=255, help_text="Tên đợt kiểm kê")
    description = models.TextField(blank=True, help_text="Mô tả chi tiết")
    
    # Phạm vi kiểm kê
    scope = models.CharField(
        max_length=20, 
        choices=AuditScope.choices, 
        default=AuditScope.FULL,
        help_text="Phạm vi kiểm kê"
    )
    departments = models.ManyToManyField(
        Department, 
        blank=True, 
        related_name='audit_sessions',
        help_text="Phòng ban cần kiểm kê (khi scope=department)"
    )
    locations = models.ManyToManyField(
        Location, 
        blank=True, 
        related_name='audit_sessions',
        help_text="Vị trí cần kiểm kê (khi scope=location)"
    )
    categories = models.ManyToManyField(
        AssetCategory, 
        blank=True, 
        related_name='audit_sessions',
        help_text="Loại tài sản cần kiểm kê (khi scope=category)"
    )
    
    # Thời gian kế hoạch
    planned_start_date = models.DateField(help_text="Ngày bắt đầu dự kiến")
    planned_end_date = models.DateField(help_text="Ngày kết thúc dự kiến")
    actual_start_date = models.DateField(null=True, blank=True, help_text="Ngày bắt đầu thực tế")
    actual_end_date = models.DateField(null=True, blank=True, help_text="Ngày kết thúc thực tế")
    
    # Trạng thái
    status = models.CharField(
        max_length=20, 
        choices=AuditSessionStatus.choices, 
        default=AuditSessionStatus.DRAFT
    )
    
    # Người tạo/phê duyệt
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_audit_sessions',
        help_text="Người tạo đợt kiểm kê"
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_audit_sessions',
        help_text="Người duyệt kế hoạch"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Thống kê (cache để tránh tính toán lại)
    total_assets = models.IntegerField(default=0, help_text="Tổng số tài sản cần kiểm kê")
    checked_assets = models.IntegerField(default=0, help_text="Số tài sản đã kiểm kê")
    matched_assets = models.IntegerField(default=0, help_text="Số tài sản khớp")
    mismatched_assets = models.IntegerField(default=0, help_text="Số tài sản chênh lệch")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đợt kiểm kê"
        verbose_name_plural = "Các đợt kiểm kê"

    def __str__(self):
        return f"{self.code} - {self.name}"

    def generate_items(self):
        """
        Tự động sinh danh sách AuditItem dựa trên scope.
        Chỉ gọi khi status = DRAFT.
        
        Returns:
            int: Số lượng items được tạo
        
        Raises:
            ValidationError: Nếu đợt kiểm kê không ở trạng thái Bản nháp
        """
        if self.status != AuditSessionStatus.DRAFT:
            raise ValidationError("Chỉ có thể sinh danh sách khi đợt kiểm kê ở trạng thái 'Bản nháp'")
        
        # Xóa items cũ (nếu có)
        self.items.all().delete()
        
        # Lọc assets theo scope
        assets = Asset.active_objects.all()
        
        if self.scope == AuditScope.DEPARTMENT and self.departments.exists():
            assets = assets.filter(current_department__in=self.departments.all())
        elif self.scope == AuditScope.LOCATION and self.locations.exists():
            assets = assets.filter(location__in=self.locations.all())
        elif self.scope == AuditScope.CATEGORY and self.categories.exists():
            assets = assets.filter(category__in=self.categories.all())
        elif self.scope == AuditScope.CUSTOM:
            # Custom scope: không tự sinh, admin chọn thủ công
            self.total_assets = 0
            self.save(update_fields=['total_assets'])
            return 0
        
        # Tạo AuditItem cho mỗi asset (snapshot dữ liệu hiện tại)
        items = []
        for asset in assets:
            items.append(AuditItem(
                audit_session=self,
                asset=asset,
                expected_location=asset.location,
                expected_department=asset.current_department,
                expected_status=asset.status,
                expected_person=asset.current_person,
                result_status=AuditResultStatus.PENDING,
            ))
        
        # Bulk create để tối ưu hiệu suất
        AuditItem.objects.bulk_create(items)
        
        # Cập nhật thống kê
        self.total_assets = len(items)
        self.checked_assets = 0
        self.matched_assets = 0
        self.mismatched_assets = 0
        self.save(update_fields=['total_assets', 'checked_assets', 'matched_assets', 'mismatched_assets'])
        
        return len(items)

    def add_items_manual(self, asset_ids):
        """
        Thêm thủ công các tài sản vào danh sách kiểm kê.
        Dùng cho scope=CUSTOM hoặc bổ sung thêm.
        
        Args:
            asset_ids: List các ID tài sản cần thêm
            
        Returns:
            int: Số lượng items được thêm
        """
        if self.status not in [AuditSessionStatus.DRAFT, AuditSessionStatus.PLANNED]:
            raise ValidationError("Chỉ có thể thêm tài sản khi đợt kiểm kê ở trạng thái 'Bản nháp' hoặc 'Đã lên kế hoạch'")
        
        # Lọc các asset chưa có trong danh sách
        existing_asset_ids = self.items.values_list('asset_id', flat=True)
        assets = Asset.active_objects.filter(id__in=asset_ids).exclude(id__in=existing_asset_ids)
        
        items = []
        for asset in assets:
            items.append(AuditItem(
                audit_session=self,
                asset=asset,
                expected_location=asset.location,
                expected_department=asset.current_department,
                expected_status=asset.status,
                expected_person=asset.current_person,
                result_status=AuditResultStatus.PENDING,
            ))
        
        AuditItem.objects.bulk_create(items)
        
        # Cập nhật thống kê
        self.total_assets = self.items.count()
        self.save(update_fields=['total_assets'])
        
        return len(items)

    def remove_items(self, item_ids):
        """
        Xóa các items khỏi danh sách kiểm kê.
        
        Args:
            item_ids: List các ID của AuditItem cần xóa
            
        Returns:
            int: Số lượng items bị xóa
        """
        if self.status not in [AuditSessionStatus.DRAFT, AuditSessionStatus.PLANNED]:
            raise ValidationError("Chỉ có thể xóa tài sản khi đợt kiểm kê ở trạng thái 'Bản nháp' hoặc 'Đã lên kế hoạch'")
        
        deleted_count, _ = self.items.filter(id__in=item_ids, result_status=AuditResultStatus.PENDING).delete()
        
        # Cập nhật thống kê
        self.total_assets = self.items.count()
        self.save(update_fields=['total_assets'])
        
        return deleted_count

    def update_statistics(self):
        """Cập nhật lại thống kê từ dữ liệu thực tế"""
        self.total_assets = self.items.count()
        self.checked_assets = self.items.exclude(result_status=AuditResultStatus.PENDING).count()
        self.matched_assets = self.items.filter(result_status=AuditResultStatus.MATCHED).count()
        self.mismatched_assets = self.checked_assets - self.matched_assets
        self.save(update_fields=['total_assets', 'checked_assets', 'matched_assets', 'mismatched_assets'])

    @property
    def progress_percent(self):
        """Tính phần trăm tiến độ kiểm kê"""
        if self.total_assets == 0:
            return 0
        return round((self.checked_assets / self.total_assets) * 100, 1)


class AuditItem(models.Model):
    """
    Chi tiết kiểm kê từng tài sản - FR4.2: Thực hiện kiểm kê
    Lưu thông tin kỳ vọng (snapshot) và kết quả thực tế
    """
    # Liên kết đợt kiểm kê
    audit_session = models.ForeignKey(
        AuditSession, 
        on_delete=models.CASCADE, 
        related_name='items',
        help_text="Đợt kiểm kê"
    )
    
    # Tài sản (có thể null nếu phát hiện tài sản thừa)
    asset = models.ForeignKey(
        Asset, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='audit_items',
        help_text="Tài sản cần kiểm kê"
    )
    
    # Thông tin kỳ vọng từ hệ thống (snapshot tại thời điểm tạo)
    expected_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='expected_audit_items',
        help_text="Vị trí theo hệ thống"
    )
    expected_department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='expected_audit_items',
        help_text="Phòng ban theo hệ thống"
    )
    expected_status = models.CharField(
        max_length=20, 
        choices=AssetStatus.choices,
        null=True,
        blank=True,
        help_text="Trạng thái theo hệ thống"
    )
    expected_person = models.ForeignKey(
        Person, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='expected_audit_items',
        help_text="Người quản lý theo hệ thống"
    )
    
    # Kết quả thực tế khi kiểm kê
    actual_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='actual_audit_items',
        help_text="Vị trí thực tế"
    )
    actual_status = models.CharField(
        max_length=20, 
        choices=AssetStatus.choices, 
        null=True, 
        blank=True,
        help_text="Trạng thái thực tế"
    )
    actual_person = models.ForeignKey(
        Person, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='actual_audit_items',
        help_text="Người đang giữ thực tế"
    )
    
    # Kết quả kiểm kê
    result_status = models.CharField(
        max_length=30, 
        choices=AuditResultStatus.choices, 
        default=AuditResultStatus.PENDING,
        help_text="Kết quả kiểm kê"
    )
    
    # Thông tin người kiểm kê
    audited_at = models.DateTimeField(null=True, blank=True, help_text="Thời điểm kiểm kê")
    auditor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audited_items',
        help_text="Người thực hiện kiểm kê"
    )
    
    # Ghi chú và hình ảnh chứng từ
    notes = models.TextField(blank=True, help_text="Ghi chú chênh lệch, mô tả")
    photo = models.ImageField(
        upload_to='audit_photos/', 
        blank=True, 
        help_text="Ảnh chụp thực tế"
    )
    
    # Thông tin quét QR/Barcode - FR4.2
    scanned_code = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Mã quét được từ QR/Barcode"
    )
    scan_method = models.CharField(
        max_length=20, 
        choices=[
            ('manual', 'Nhập thủ công'),
            ('qr', 'Quét mã QR'),
            ('barcode', 'Quét Barcode'),
        ], 
        default='manual',
        help_text="Phương thức nhập liệu"
    )

    class Meta:
        ordering = ['audit_session', 'id']
        verbose_name = "Chi tiết kiểm kê"
        verbose_name_plural = "Chi tiết kiểm kê"
        # Đảm bảo mỗi asset chỉ xuất hiện 1 lần trong mỗi đợt kiểm kê
        unique_together = ['audit_session', 'asset']

    def __str__(self):
        asset_name = self.asset.name if self.asset else "Tài sản thừa"
        return f"{self.audit_session.code} - {asset_name}"

    def check_asset(self, auditor, actual_location=None, actual_status=None, actual_person=None, 
                    notes='', photo=None, scan_method='manual', scanned_code=''):
        """
        Ghi nhận kết quả kiểm kê cho tài sản - FR4.2
        
        Args:
            auditor: User thực hiện kiểm kê
            actual_location: Vị trí thực tế
            actual_status: Trạng thái thực tế
            actual_person: Người đang giữ thực tế
            notes: Ghi chú
            photo: Ảnh chụp
            scan_method: Phương thức quét (manual/qr/barcode)
            scanned_code: Mã quét được
        """
        self.auditor = auditor
        self.audited_at = timezone.now()
        self.actual_location = actual_location
        self.actual_status = actual_status
        self.actual_person = actual_person
        self.notes = notes
        self.scan_method = scan_method
        self.scanned_code = scanned_code
        
        if photo:
            self.photo = photo
        
        # Xác định kết quả
        self.result_status = self._determine_result_status()
        
        self.save()
        
        # Cập nhật thống kê của đợt kiểm kê
        self.audit_session.update_statistics()
        
        return self.result_status

    def _determine_result_status(self):
        """Xác định kết quả kiểm kê dựa trên so sánh kỳ vọng và thực tế"""
        # Nếu không tìm thấy tài sản
        if self.actual_status == AssetStatus.BROKEN and self.expected_status != AssetStatus.BROKEN:
            return AuditResultStatus.DAMAGED
        
        # So sánh các thuộc tính
        location_match = (self.actual_location_id == self.expected_location_id) or \
                         (self.actual_location is None and self.expected_location is None)
        status_match = (self.actual_status == self.expected_status) or \
                       (self.actual_status is None)
        person_match = (self.actual_person_id == self.expected_person_id) or \
                       (self.actual_person is None and self.expected_person is None)
        
        # Xác định loại chênh lệch
        if not location_match:
            return AuditResultStatus.LOCATION_MISMATCH
        if not status_match:
            return AuditResultStatus.STATUS_MISMATCH
        if not person_match:
            return AuditResultStatus.PERSON_MISMATCH
        
        return AuditResultStatus.MATCHED

    def mark_as_missing(self, auditor, notes=''):
        """Đánh dấu tài sản không tìm thấy"""
        self.auditor = auditor
        self.audited_at = timezone.now()
        self.result_status = AuditResultStatus.MISSING
        self.notes = notes or "Không tìm thấy tài sản tại vị trí"
        self.save()
        self.audit_session.update_statistics()


class AuditAction(models.Model):
    """
    Đề xuất xử lý chênh lệch - FR4.3: Đề xuất xử lý
    Theo dõi các hành động cần thực hiện sau kiểm kê
    """
    audit_item = models.ForeignKey(
        AuditItem, 
        on_delete=models.CASCADE, 
        related_name='actions',
        help_text="Chi tiết kiểm kê liên quan"
    )
    
    # Loại đề xuất
    action_type = models.CharField(
        max_length=30, 
        choices=AuditActionType.choices,
        help_text="Loại đề xuất xử lý"
    )
    description = models.TextField(help_text="Mô tả chi tiết đề xuất")
    
    # Trạng thái xử lý
    status = models.CharField(
        max_length=20, 
        choices=AuditActionStatus.choices, 
        default=AuditActionStatus.PROPOSED
    )
    
    # Người đề xuất/duyệt/thực hiện
    proposed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='proposed_audit_actions',
        help_text="Người đề xuất"
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_audit_actions',
        help_text="Người duyệt"
    )
    executed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executed_audit_actions',
        help_text="Người thực hiện"
    )
    
    # Thời gian
    proposed_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    # Ghi chú từ chối (nếu có)
    rejection_note = models.TextField(blank=True, help_text="Lý do từ chối")
    
    # Liên kết kết quả thực hiện
    result_ticket = models.ForeignKey(
        'TicketRequest', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='from_audit_actions',
        help_text="Ticket được tạo từ đề xuất này"
    )
    result_history = models.ForeignKey(
        'AssetHistory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='from_audit_actions',
        help_text="Lịch sử tài sản được tạo từ đề xuất này"
    )

    class Meta:
        ordering = ['-proposed_at']
        verbose_name = "Đề xuất xử lý kiểm kê"
        verbose_name_plural = "Các đề xuất xử lý kiểm kê"

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.audit_item}"

    def approve(self, user, note=''):
        """Duyệt đề xuất"""
        if self.status != AuditActionStatus.PROPOSED:
            raise ValidationError("Chỉ có thể duyệt đề xuất đang ở trạng thái 'Đề xuất'")
        
        self.status = AuditActionStatus.APPROVED
        self.approved_by = user
        self.approved_at = timezone.now()
        if note:
            self.description += f"\n[Ghi chú duyệt]: {note}"
        self.save()

    def reject(self, user, reason):
        """Từ chối đề xuất"""
        if self.status != AuditActionStatus.PROPOSED:
            raise ValidationError("Chỉ có thể từ chối đề xuất đang ở trạng thái 'Đề xuất'")
        
        self.status = AuditActionStatus.REJECTED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.rejection_note = reason
        self.save()

    def execute(self, user):
        """Đánh dấu đã thực hiện đề xuất"""
        if self.status != AuditActionStatus.APPROVED:
            raise ValidationError("Chỉ có thể thực hiện đề xuất đã được duyệt")
        
        self.status = AuditActionStatus.EXECUTED
        self.executed_by = user
        self.executed_at = timezone.now()
        self.save()


# Alias để backward compatibility với code cũ
# Có thể xóa sau khi migrate xong
class AssetAudit(AuditItem):
    """
    [DEPRECATED] Sử dụng AuditItem thay thế.
    Class này chỉ để backward compatibility.
    """
    class Meta:
        proxy = True
        verbose_name = "[Deprecated] Kiểm kê cũ"