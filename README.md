# DRF Backend for Asset Management System

This project sets up a full-stack Django Rest Framework application, powered by:

- DRF 3.16.1
- PostgreSQL 15 (docker container)

---

## Prerequisites

- Python 3.10 or higher
- Check your Python version:
  python -V

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/noc2-itdev/asset_mgn.git
```

### 2. Create and install packages in venv

```bash
python -m venv venv
venv\Scripts\activate.bat  (Os Windows)
source venv/bin/activate  (Os Linux)
python -m pip install -r requirements.txt
```

### 3. Create and run project Django

```bash
python manage.py startproject asset_mgn .
python manage.py runserver 0.0.0.0:8000
```

### 4. Access the application

```bash
http://localhost:8000
```

### 5. Create .env file in the root directory of your project and add the following environment variables:

```bash
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
DATABASE_NAME=asset_mgn
DATABASE_USER=noc2_user
DATABASE_PASSWORD=asset_mgn_password
DATABASE_HOST=X.X.X.X
DATABASE_PORT=5432
```



