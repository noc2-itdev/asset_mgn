# 📋 TÀI LIỆU DỰ ÁN QUẢN LÝ TÀI SẢN NOC2

> **Phiên bản:** 1.2  
> **Cập nhật:** 2026-01-07  
> **Mục đích:** Tổng hợp cấu trúc models, thiết kế chức năng và phân công Git branches

---

## 📊 I. CẤU TRÚC MODELS

### 1.1 Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CẤU TRÚC DỮ LIỆU                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│   │  Department  │  │   Person     │  │   Location   │             │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│          │                 │                 │                      │
│          └─────────────────┼─────────────────┘                      │
│                            ▼                                        │
│                    ┌──────────────┐                                 │
│   AssetCategory ──▶│    Asset     │◀── AssetAttachment             │
│                    └──────┬───────┘                                 │
│                           │                                         │
│          ┌────────────────┼────────────────┐                        │
│          ▼                ▼                ▼                        │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│   │AssetHistory │  │TicketRequest│  │ AuditItem   │                │
│   └─────────────┘  └─────────────┘  └──────┬──────┘                │
│                                            │                        │
│                    ┌───────────────────────┼───────────────┐        │
│                    ▼                       │               ▼        │
│            ┌──────────────┐               │       ┌──────────────┐ │
│            │ AuditSession │◀──────────────┘       │ AuditAction  │ │
│            └──────────────┘                       └──────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Danh sách Models (13 models)

| STT | Model | Mô tả | Loại |
|-----|-------|-------|------|
| 1 | `Department` | Đơn vị/Phòng ban | Danh mục |
| 2 | `Person` | Cá nhân chịu trách nhiệm | Danh mục |
| 3 | `Location` | Vị trí/địa điểm lắp đặt | Danh mục |
| 4 | `AssetCategory` | Loại tài sản | Danh mục |
| 5 | `Asset` | Tài sản chính | Core |
| 6 | `AssetAttachment` | Tài liệu đính kèm | Core |
| 7 | `AssetHistory` | Lịch sử biến động | Tracking |
| 8 | `TicketRequest` | Yêu cầu sửa chữa/bảo trì | Workflow |
| 9 | `AuditSession` | Đợt kiểm kê | Audit (MỚI) |
| 10 | `AuditItem` | Chi tiết kiểm kê từng TS | Audit (MỚI) |
| 11 | `AuditAction` | Đề xuất xử lý chênh lệch | Audit (MỚI) |

---

## 🔍 II. CHỨC NĂNG KIỂM KÊ (FR4)

### 2.1 Workflow kiểm kê

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LUỒNG KIỂM KÊ TÀI SẢN                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ① TẠO ĐỢT (DRAFT)                                                 │
│     └─► Chọn scope (full/department/location/category/custom)      │
│                                                                     │
│  ② SINH DANH SÁCH                                                  │
│     └─► generate_items() → Tự động tạo AuditItem theo scope        │
│     └─► add_items_manual() → Thêm thủ công (nếu scope=custom)      │
│                                                                     │
│  ③ DUYỆT KẾ HOẠCH (PLANNED)                                        │
│     └─► Xem lại danh sách, phân công người kiểm kê                 │
│                                                                     │
│  ④ THỰC HIỆN (IN_PROGRESS)                                         │
│     └─► Quét QR/Barcode hoặc nhập thủ công                         │
│     └─► check_asset() → Ghi nhận kết quả, so sánh chênh lệch       │
│                                                                     │
│  ⑤ HOÀN THÀNH (COMPLETED)                                          │
│     └─► Tổng hợp thống kê, xuất biên bản                           │
│     └─► Tạo AuditAction cho các chênh lệch                         │
│                                                                     │
│  ⑥ XỬ LÝ CHÊNH LỆCH                                                │
│     └─► Duyệt/Từ chối đề xuất                                      │
│     └─► Thực hiện: cập nhật Asset, tạo TicketRequest...            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Các loại Scope (phạm vi kiểm kê)

| Scope | Hành vi |
|-------|---------|
| `full` | Tự động lấy TẤT CẢ tài sản đang hoạt động |
| `department` | Tự động lấy theo phòng ban được chọn |
| `location` | Tự động lấy theo vị trí được chọn |
| `category` | Tự động lấy theo loại tài sản được chọn |
| `custom` | KHÔNG tự sinh, người dùng chọn thủ công |

### 2.3 Các loại kết quả kiểm kê (AuditResultStatus)

| Kết quả | Mô tả |
|---------|-------|
| `pending` | Chưa kiểm kê |
| `matched` | Khớp với hệ thống |
| `location_mismatch` | Sai vị trí |
| `status_mismatch` | Sai trạng thái |
| `person_mismatch` | Sai người quản lý |
| `missing` | Không tìm thấy |
| `damaged` | Phát hiện hư hỏng mới |
| `excess` | Tài sản thừa (không có trong hệ thống) |

### 2.4 Các loại đề xuất xử lý (AuditActionType)

| Loại | Mô tả |
|------|-------|
| `update_location` | Cập nhật vị trí trong hệ thống |
| `update_status` | Cập nhật trạng thái |
| `update_person` | Cập nhật người quản lý |
| `report_missing` | Báo mất tài sản |
| `repair` | Tạo yêu cầu sửa chữa |
| `liquidate` | Đề xuất thanh lý |
| `compensate` | Yêu cầu bồi thường |
| `create_new` | Tạo mới tài sản thừa |
| `no_action` | Không cần xử lý |

---

## 📡 III. API ENDPOINTS

### 3.1 Audit Session (Đợt kiểm kê)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| GET, POST | `/api/audit-sessions/` | Danh sách & tạo đợt |
| GET, PUT, PATCH | `/api/audit-sessions/<id>/` | Chi tiết & cập nhật |
| POST | `/api/audit-sessions/<id>/generate-items/` | Sinh danh sách tự động |
| POST | `/api/audit-sessions/<id>/add-items/` | Thêm TS thủ công |
| DELETE | `/api/audit-sessions/<id>/remove-items/` | Xóa TS khỏi danh sách |
| POST | `/api/audit-sessions/<id>/start/` | Bắt đầu kiểm kê |
| POST | `/api/audit-sessions/<id>/complete/` | Hoàn thành |
| GET | `/api/audit-sessions/<id>/report/` | Xuất biên bản |

### 3.2 Audit Item (Chi tiết kiểm kê)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| GET | `/api/audit-sessions/<id>/items/` | Danh sách TS cần kiểm |
| POST | `/api/audit-items/<id>/check/` | Ghi nhận kiểm kê |
| POST | `/api/audit-items/<id>/mark-missing/` | Đánh dấu không tìm thấy |

### 3.3 Audit Action (Đề xuất xử lý)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| POST | `/api/audit-items/<id>/actions/` | Tạo đề xuất |
| POST | `/api/audit-actions/<id>/approve/` | Duyệt |
| POST | `/api/audit-actions/<id>/reject/` | Từ chối |
| POST | `/api/audit-actions/<id>/execute/` | Thực hiện |

---

## � IV. PHÂN CÔNG GIT BRANCHES

### 4.1 Master Data (Dev A)

| Branch | Files | Chức năng |
|--------|-------|-----------|
| `feature/master-department` | `department/` | **CRUD Phòng ban** - Quản lý đơn vị/phòng ban. Computed: số TS, số nhân viên |
| `feature/master-location` | `location/` | **CRUD Vị trí** - Quản lý địa điểm lắp đặt. Computed: số TS tại vị trí |
| `feature/master-person` | `person/` | **CRUD Cá nhân** - Quản lý người dùng. Filter theo phòng ban. Computed: số TS đang quản lý |
| `feature/master-category` | `category/` | **CRUD Loại TS** - Phân loại (máy tính, RAM...). Field `is_component` xác định linh kiện |

### 4.2 Asset (Dev B)

| Branch | Files | Chức năng |
|--------|-------|-----------|
| `feature/asset-crud` | `asset/views/asset_views.py` | **CRUD Tài sản** - Thêm/sửa/xóa (soft)/xem. Search, filter. **QR Lookup**, **Lịch sử** |
| `feature/asset-component` | `asset/views/component_views.py` | **Quản lý linh kiện** - Xem components. **Upgrade** - lắp linh kiện. **Retrieve** - tháo linh kiện |
| `feature/asset-transfer` | `asset/views/transfer_views.py` | **Bàn giao** - Chuyển đổi phòng/người/vị trí, ghi log. **File đính kèm** - Upload tài liệu |

### 4.3 Audit (Dev C)

| Branch | Files | Chức năng |
|--------|-------|-----------|
| `feature/audit-session` | `audit/views/session_views.py` | **Đợt kiểm kê** - CRUD Session. **generate_items** theo scope. **Workflow** start/complete. **Export report** |
| `feature/audit-item` | `audit/views/item_views.py` | **Chi tiết kiểm kê** - Danh sách items. Thêm/xóa thủ công. **check_item** - so sánh expected vs actual |
| `feature/audit-action` | `audit/views/action_views.py` | **Xử lý chênh lệch** - Tạo đề xuất. **approve/reject**. **execute** - cập nhật Asset, tạo TicketRequest |

### 4.4 Ticket (Dev D)

| Branch | Files | Chức năng |
|--------|-------|-----------|
| `feature/ticket-crud` | `ticket_request/views/` | **Yêu cầu sửa chữa/bảo trì** - CRUD Ticket. **Workflow** approve/reject/complete. Cập nhật Asset.status |

### 4.5 Sơ đồ dependency

```
master-department ─┐
master-location   ─┼──► asset-crud ──┬──► asset-component
master-person     ─┤                 ├──► asset-transfer
master-category   ─┘                 │
                                     ▼
                            audit-session
                                 │
                                 ▼
                            audit-item
                                 │
                                 ▼
                            audit-action ──► ticket-crud
```

---

## �📝 V. CHANGELOG

| Ngày | Phiên bản | Thay đổi |
|------|-----------|----------|
| 2026-01-07 | 1.2 | Thêm mô tả chi tiết 11 Git branches |
| 2026-01-06 | 1.1 | Thêm models kiểm kê: `AuditSession`, `AuditItem`, `AuditAction` |
| 2026-01-06 | 1.0 | Khởi tạo tài liệu |
