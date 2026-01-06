# 📋 TÀI LIỆU DỰ ÁN QUẢN LÝ TÀI SẢN NOC2

> **Phiên bản:** 2.1 | **Cập nhật:** 2026-01-06

---

## I. CẤU TRÚC SCAFFOLD ĐÃ TẠO

### Tổng quan: 7 apps, 34 files

| App | Views | Serializers | URLs | Branch |
|-----|-------|-------------|------|--------|
| **audit** | 3 files | 3 files | 3 files | `feature/audit-*` |
| **asset** | 3 files | 2 files | 3 files | `feature/asset-*` |
| **ticket_request** | 1 file | 1 file | 1 file | `feature/ticket-*` |
| **department** | 1 file | 1 file | 1 file | `feature/master-department` |
| **location** | 1 file | 1 file | 1 file | `feature/master-location` |
| **person** | 1 file | 1 file | 1 file | `feature/master-person` |
| **category** | 1 file | 1 file | 1 file | `feature/master-category` |

---

## II. PHÂN CÔNG CÔNG VIỆC

### Dev A: Master Data (4 apps đơn giản)

| Branch | App | Endpoints |
|--------|-----|-----------|
| `feature/master-department` | department | CRUD |
| `feature/master-location` | location | CRUD |
| `feature/master-person` | person | CRUD + filter by dept |
| `feature/master-category` | category | CRUD |

### Dev B: Asset (1 app phức tạp)

| Branch | File | Endpoints |
|--------|------|-----------|
| `feature/asset-crud` | `asset_views.py` | CRUD, QR lookup, history |
| `feature/asset-component` | `component_views.py` | components, upgrade, retrieve |
| `feature/asset-transfer` | `transfer_views.py` | transfer, attachments |

### Dev C: Audit (1 app phức tạp)

| Branch | File | Endpoints |
|--------|------|-----------|
| `feature/audit-session` | `session_views.py` | CRUD session, generate, start, complete |
| `feature/audit-item` | `item_views.py` | list items, check, mark-missing |
| `feature/audit-action` | `action_views.py` | create, approve, reject, execute |

### Dev D: Ticket Request

| Branch | File | Endpoints |
|--------|------|-----------|
| `feature/ticket-crud` | `ticket_views.py` | CRUD, approve, reject, complete |

---

## III. QUY TẮC GIT

### Branch naming
```
feature/<app>-<tính_năng>
VD: feature/asset-crud, feature/audit-session
```

### Commit message
```
[app] type: description
VD: [asset] feat: implement transfer endpoint
```

### Merge flow
```
feature/* → develop → main
```

---

## IV. CẤU TRÚC THƯ MỤC

```
asset_mgn/
├── audit/
│   ├── views/
│   │   ├── session_views.py   # Dev C
│   │   ├── item_views.py      # Dev C
│   │   └── action_views.py    # Dev C
│   ├── serializers/
│   └── urls/
│
├── asset/
│   ├── views/
│   │   ├── asset_views.py     # Dev B
│   │   ├── component_views.py # Dev B
│   │   └── transfer_views.py  # Dev B
│   ├── serializers/
│   └── urls/
│
├── ticket_request/
│   ├── views/
│   │   └── ticket_views.py    # Dev D
│   ├── serializers/
│   └── urls/
│
├── department/                 # Dev A (đơn giản)
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── location/                   # Dev A
├── person/                     # Dev A
└── category/                   # Dev A
```

---

## V. HƯỚNG DẪN CHO DEV

### Bước 1: Checkout nhánh
```bash
git checkout develop
git pull origin develop
git checkout -b feature/<app>-<tính_năng>
```

### Bước 2: Implement logic
- Tìm các comment `# TODO: Implement`
- Đọc docstring để hiểu input/output mong muốn
- Implement theo logic đã mô tả

### Bước 3: Commit và push
```bash
git add .
git commit -m "[app] feat: implement xxx"
git push origin feature/<app>-<tính_năng>
```

### Bước 4: Tạo Pull Request
- Target: `develop`
- Assign reviewer: Team Lead

---

## VI. CHANGELOG

| Ngày | Ver | Thay đổi |
|------|-----|----------|
| 2026-01-06 | 2.1 | Tạo scaffold đầy đủ cho 7 apps (34 files) |
| 2026-01-06 | 2.0 | Chiến lược phân chia, scaffold audit app |
| 2026-01-06 | 1.x | Thiết kế models, AssetAction |
