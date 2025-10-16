# DRF Backend for Asset Management System

This project sets up a full-stack Django Rest Framework application, powered by:

- DRF 3.16.1
- PostgreSQL 15

---

## Prerequisites
- Python 3.10 or higher
- Check your Python version:
python -V

---

## 🛠 Setup Instructions

### 1. Clone the repository
git clone https://github.com/noc2-itdev/asset_mgn.git

### 2. Create and install packages in venv
python -m venv venv

venv\Scripts\activate.bat  (Os Windows)

source venv/bin/activate  (Os Linux)

python -m pip install -r requirements.txt

### 3. Create and run project Django
python manage.py startproject asset_mgn .

python manage.py runserver 0.0.0.0:8000

### 4. Access the application
http://localhost:8000



