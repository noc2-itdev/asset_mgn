from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File


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
        help_text="Đánh dấu nếu đây là linh kiện có thể tách rời và chuyển giao (RAM, SSD, Card màn hình)"
    )  # True cho RAM, SSD; False cho Máy tính
    def __str__(self):
        return self.name


# Tài sản: máy tính, máy in,...
class Asset(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('AssetCategory', on_delete=models.SET_NULL, null=True)
    parent_asset = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='components',  # Tên ngược lại (Ví dụ: computer.components.all())
        help_text="Chỉ định tài sản cấp trên (Ví dụ: RAM thuộc về Máy tính nào)"
    )
    asset_code = models.CharField(max_length=100, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    status = models.CharField(max_length=20, choices=AssetStatus.choices, default=AssetStatus.IN_USE)
    current_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    current_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    acquisition_type = models.CharField(max_length=50, choices=[
        ('purchase', 'Mua sắm'),
        ('transfer', 'Điều chuyển'),
        ('donation', 'Tiếp nhận')
    ])  # hình thức tiếp nhận: xác định phương thức mà tài sản được đưa vào quyền quản lý của đơn vị
    acquisition_date = models.DateField()  # thời điểm tài sản được đưa vào sử dụng hoặc chính thức thuộc quyền quản lý
    purchase_date = models.DateField()
    warranty_expiry = models.DateField(null=True, blank=True)

    # Tối ưu hóa truy vấn tìm kiếm theo asset_code, category và current_department
    class Meta:
        indexes = [
            models.Index(fields=['asset_code']),
            models.Index(fields=['category']),
            models.Index(fields=['current_department']),
        ]

    def clean(self):
        # Ngăn asset tham chiếu chính nó
        if self.parent_asset and self.parent_asset == self:
            raise ValidationError("Tài sản không thể thuộc về chính nó.")

    def save(self, *args, **kwargs):
        if not self.qr_code and self.asset_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.asset_code) # Đã sửa
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')

            self.qr_code.save(f'qr_{self.asset_code}.png', # Đã sửa
                              File(buffer), save=False)
        self.clean()  # đảm bảo kiểm tra trước khi lưu
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.asset_code})"


class AssetAction(models.TextChoices):
    TRANSFER = 'transfer', 'Bàn giao'
    REPAIR = 'repair', 'Sửa chữa'
    UPGRADE = 'upgrade', 'Nâng cấp'
    MOVE = 'move', 'Di dời'
    RETRIEVE = 'retrieve', 'Thu hồi'


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

    def __str__(self):
        return f"{self.asset} - {self.action} - {self.date}"


class RepairRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Chờ xử lý'
    IN_PROGRESS = 'in_progress', 'Đang xử lý'
    COMPLETED = 'completed', 'Hoàn thành'
    REJECTED = 'rejected', 'Từ chối'


# RepairRequest: Quản lý yêu cầu sửa chữa
class RepairRequest(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repair_requests')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=RepairRequestStatus.choices, default=RepairRequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_requests')
    resolution_note = models.TextField(blank=True)

    def __str__(self):
        return f"Yêu cầu sửa chữa: {self.asset} - {self.get_status_display()}"


# AssetAudit: Kiểm kê tài sản thực tế
class AssetAudit(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, on_delete=models.CASCADE)
    audit_date = models.DateTimeField(auto_now_add=True)
    physical_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=AssetStatus.choices)
    is_matching = models.BooleanField()  # True nếu dữ liệu thực tế khớp với hệ thống
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Kiểm kê: {self.asset} - {self.audit_date}"
