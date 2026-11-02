# FinTrack — Smart Expense & Financial Insights System

A Django + MySQL personal finance application with authentication, transaction CRUD, category tracking, budgets, dashboard charts and yearly reports.

## Requirements
- Python 3.10+
- MySQL Server 8+
- Node.js is NOT required (Bootstrap and Chart.js are loaded from CDN).

## Setup (Windows / VS Code)

1. Open this folder in VS Code.
2. Create and activate a virtual environment:
   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```
4. In MySQL Workbench or MySQL command line, create the database:
   ```sql
   CREATE DATABASE smart_expense_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. Configure database credentials in `config/settings.py`, or set environment variables:
   ```powershell
   $env:DB_NAME="smart_expense_db"
   $env:DB_USER="root"
   $env:DB_PASSWORD="your_mysql_password"
   $env:DB_HOST="127.0.0.1"
   $env:DB_PORT="3306"
   ```
6. Create database tables:
   ```powershell
   py manage.py makemigrations expenses
   py manage.py migrate
   ```
7. Create admin user (optional):
   ```powershell
   py manage.py createsuperuser
   ```
8. Run:
   ```powershell
   py manage.py runserver
   ```
9. Open http://127.0.0.1:8000/ and create an account.

## Notes
- New users automatically receive starter income and expense categories.
- All transaction and budget queries are scoped to the signed-in user.
- This is a learning portfolio starter. Before public deployment, set DEBUG=False, use a strong SECRET_KEY, configure ALLOWED_HOSTS, HTTPS, secure cookies, environment-based secrets and production static files.
