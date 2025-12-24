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
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )

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
    IN_USE = "in_use", "Đang sử dụng"
    IN_STORAGE = "in_storage", "Lưu kho"
    LIQUIDATED = "liquidated", "Thanh lý"
    BROKEN = "broken", "Hư hỏng"


# AssetCategory: phân loại linh kiện và tài sản chính. (máy tính, máy in, RAM, SSD,...).
class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_component = models.BooleanField(
        default=False,
        help_text="Đánh dấu nếu đây là linh kiện có thể tách rời khỏi thiết bị (RAM, SSD, Card màn hình)",
    )  # True cho RAM, SSD; False cho Máy tính

    def __str__(self):
        return self.name


# Tài sản: máy tính, máy in,...
class Asset(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey("AssetCategory", on_delete=models.SET_NULL, null=True)
    parent_asset = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="components",  # Tên ngược lại (Ví dụ: computer.components.all())
        help_text="Chỉ định tài sản cấp trên (Ví dụ: RAM thuộc về Máy tính nào)",
    )
    asset_code = models.CharField(max_length=100, unique=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True)
    status = models.CharField(
        max_length=20, choices=AssetStatus.choices, default=AssetStatus.IN_STORAGE
    )
    current_department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    current_person = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(blank=True)
    acquisition_type = models.CharField(
        max_length=50,
        choices=[
            ("purchase", "Mua sắm"),
            ("transfer", "Điều chuyển"),  # từ nội bộ
            ("donation", "Tiếp nhận"),  # từ đơn vị ngoài
        ],
    )  # hình thức tiếp nhận: xác định phương thức mà tài sản được đưa vào quyền quản lý của đơn vị
    acquisition_date = models.DateField(
        null=True, blank=True
    )  # thời điểm tài sản được đưa vào sử dụng hoặc chính thức thuộc quyền quản lý
    purchase_date = models.DateField(
        null=True, blank=True
    )  # thời điểm mua sắm hoặc tiếp nhận tài sản
    warranty_expiry = models.DateField(null=True, blank=True)
    has_independent_value = models.BooleanField(
        default=True,
        help_text="True nếu tài sản có giá trị độc lập cần đối soát với kế toán",
    )
    serial_number = models.CharField(
        max_length=100, blank=True, help_text="Số serial của thiết bị"
    )
    model = models.CharField(max_length=100, blank=True, help_text="Model thiết bị")
    vendor = models.CharField(
        max_length=255, blank=True, help_text="Nhà cung cấp, phân phối"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Vị trí hiện tại của tài sản",
    )
    value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Giá trị tài sản (VNĐ)",
    )
    is_deleted = models.BooleanField(default=False)  # soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def delete(self):
        """Soft delete - chỉ đánh dấu đã xóa"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_deleted=False)

    objects = models.Manager()  # Manager mặc định, truy vấn tất cả bản ghi
    active_objects = ActiveManager()  # Manager custom chỉ lấy bản ghi chưa xóa

    # Tối ưu hóa truy vấn tìm kiếm theo asset_code, category, current_department và location
    class Meta:
        indexes = [
            models.Index(fields=["asset_code"]),
            models.Index(fields=["category"]),
            models.Index(fields=["current_department"]),
            models.Index(fields=["location"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        # Ngăn asset tham chiếu chính nó
        if self.parent_asset and self.parent_asset == self:
            raise ValidationError("Tài sản không thể thuộc về chính nó.")

    def save(self, *args, **kwargs):
        if not self.qr_code and self.asset_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.asset_code)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")

            self.qr_code.save(f"qr_{self.asset_code}.png", File(buffer), save=False)
        self.clean()  # đảm bảo kiểm tra trước khi lưu
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.asset_code})"

    @property
    def is_component(self):
        """Xác định tài sản có phải là component dựa trên danh mục"""
        return self.category.is_component


# AssetAttachment: Tài liệu đính kèm để 1 tài sản có thể lưu trữ nhiều file cùng lúc như hóa đơn mua sắm, giấy tờ thanh lý,...
class AssetAttachment(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="asset_attachments/")
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.asset_code} - {self.file.name}"


class AssetAction(models.TextChoices):
    TRANSFER = "transfer", "Bàn giao"
    REPAIR = "repair", "Sửa chữa"
    BORROW = "borrow", "Cho mượn"
    MAINTENANCE = "maintenance", "Bảo trì"
    UPGRADE = "upgrade", "Nâng cấp"
    RETRIEVE = "retrieve", "Thu hồi"
    CREATE = "create", "Tạo mới"
    UPDATE = "update", "Cập nhật thông tin"
    AUDIT = "audit", "Kiểm kê"
    STATUS_CHANGE = "status_change", "Thay đổi trạng thái"
    LOCATION_CHANGE = "location_change", "Thay đổi vị trí"


# Lưu lịch sử thay đổi của tài sản (bàn giao, sửa chữa, di dời, ...).
class AssetHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="histories")
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(
        max_length=20, choices=AssetAction.choices, default=AssetAction.TRANSFER
    )
    from_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="from_histories",
    )
    to_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="to_histories",
    )
    from_person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="from_person_histories",
    )
    to_person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="to_person_histories",
    )
    note = models.TextField(blank=True)
    from_status = models.CharField(
        max_length=20, choices=AssetStatus.choices, null=True, blank=True
    )
    to_status = models.CharField(
        max_length=20, choices=AssetStatus.choices, null=True, blank=True
    )
    from_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="from_histories",
    )
    to_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="to_histories",
    )
    related_ticket = models.ForeignKey(
        "TicketRequest", on_delete=models.SET_NULL, null=True, blank=True
    )
    related_audit = models.ForeignKey(
        "AssetAudit", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.asset} - {self.action} - {self.date}"


class TicketRequestStatus(models.TextChoices):
    PENDING = "pending", "Chờ xử lý"
    IN_PROGRESS = "in_progress", "Đang xử lý"
    COMPLETED = "completed", "Hoàn thành"
    REJECTED = "rejected", "Từ chối"


# TicketRequest: Quản lý yêu cầu sửa chữa/bảo trì từ tài sản thuộc bản thân quản lý hoặc yêu cầu mượn tài sản từ kho
class TicketRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("repair", "Sửa chữa"),
        ("borrow", "Mượn tài sản"),
        ("maintenance", "Bảo trì"),
    ]

    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ticket_requests"
    )
    request_type = models.CharField(
        max_length=20, choices=REQUEST_TYPE_CHOICES, default="repair"
    )
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=TicketRequestStatus.choices,
        default=TicketRequestStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handler = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="handled_tickets",
    )
    resolution_note = models.TextField(blank=True)
    # Các trường dùng cho bảo trì định kỳ
    scheduled_date = models.DateField(
        null=True, blank=True, help_text="Ngày dự kiến thực hiện"
    )
    frequency = models.CharField(
        max_length=20,
        choices=[
            ("monthly", "Hàng tháng"),
            ("quarterly", "Hàng quý"),
            ("semi_annual", "6 tháng"),
            ("annual", "Hàng năm"),
        ],
        null=True,
        blank=True,
        help_text="Tần suất bảo trì",
    )
    is_recurring = models.BooleanField(
        default=False, help_text="Là yêu cầu bảo trì định kỳ"
    )  # True: Hệ thống có thể lên lịch tự động tạo ticket bảo trì cho các tài sản cần bảo trì định kỳ
    next_maintenance_date = models.DateField(
        null=True, blank=True, help_text="Ngày bảo trì tiếp theo"
    )

    def __str__(self):
        return (
            f"Yêu cầu {self.request_type}: {self.asset} - {self.get_status_display()}"
        )


# AssetAudit: Kiểm kê tài sản thực tế
class AssetAudit(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, on_delete=models.CASCADE)
    audit_date = models.DateTimeField(auto_now_add=True)
    physical_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Vị trí thực tế khi kiểm kê",
    )
    status = models.CharField(max_length=20, choices=AssetStatus.choices)
    is_matching = models.BooleanField()  # True nếu dữ liệu thực tế khớp với hệ thống
    notes = models.TextField(blank=True)  # ghi chú chênh lệch (thiếu, hỏng, đúng)

    def __str__(self):
        return f"Kiểm kê: {self.asset} - {self.audit_date}"


# UPDATE MODEL v1
class AssetAttribute(models.Model):
    category = models.ForeignKey(
        AssetCategory, on_delete=models.CASCADE, related_name="attributes"
    )
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    data_type = models.CharField(
        max_length=20,
        choices=[
            ("string", "String"),
            ("number", "Number"),
            ("date", "Date"),
            ("boolean", "Boolean"),
        ],
    )
    is_required = models.BooleanField(default=False)


class AssetAttributeValue(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="attribute_values"
    )
    attribute = models.ForeignKey(AssetAttribute, on_delete=models.CASCADE)
    value = models.TextField()


# Phiếu nhập tài sản (FR2)
class AssetReceipt(models.Model):
    receipt_code = models.CharField(max_length=50, unique=True)
    supplier = models.CharField(max_length=255)
    receipt_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(blank=True)


class AssetReceiptItem(models.Model):
    receipt = models.ForeignKey(
        AssetReceipt, on_delete=models.CASCADE, related_name="items"
    )
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
