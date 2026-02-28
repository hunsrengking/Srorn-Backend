# cPanel MySQL Database Connection Guide

## Step 1: Create Database in cPanel

1. Go to **cPanel → MySQL Databases**
2. Create a new database:
   - Database Name: `username_support_system` (cPanel adds your username prefix)
   - Click **Create Database**

3. Create a new MySQL user:
   - Go to **cPanel → MySQL Users**
   - Username: `username_dbuser` (e.g., `abc123_dbuser`)
   - Password: Generate a strong password
   - Click **Create User**

4. Add privileges:
   - Go back to **MySQL Databases**
   - Select your database and user
   - Check all privileges (or at minimum: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX)
   - Click **Add User to Database**

---

## Step 2: Update .env File for cPanel

Replace your `.env` file with these values from cPanel:

```env
# Database Configuration (from cPanel MySQL section)
DB_USER=username_dbuser
DB_PASSWORD=your_generated_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=username_support_system

# Application Settings
SECRET_KEY=your-super-secret-key-change-this
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=change-this-password

# Frontend URL (your domain)
FRONTEND_URL=https://yourdomain.com

# Company Settings
COMPANY_NAME=Support System
COMPANY_PRIMARY_COLOR=#0F766E
COMPANY_LOGO_URL=https://yourdomain.com/logo.png

# Email Configuration (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-specific-password
SYSTEM_EMAIL=your-email@gmail.com
```

---

## Step 3: Key Differences from Local Development

| Setting | Local Development | cPanel Production |
|---------|------------------|-------------------|
| DB_HOST | 127.0.0.1 or localhost | localhost |
| DB_PORT | 3309 (your custom port) | 3306 (cPanel standard) |
| DB_USER | root | username_dbuser |
| FRONTEND_URL | http://127.0.0.1:5173 | https://yourdomain.com |
| SMTP_HOST | Your local/test SMTP | smtp.gmail.com |

---

## Step 4: Test Database Connection via SSH

```bash
# SSH into cPanel
ssh username@yourdomain.com

# Navigate to your app directory
cd public_html/your_app_folder

# Test MySQL connection
mysql -u username_dbuser -p -h localhost username_support_system
```

If connection succeeds, you'll see: `mysql>`

Type `exit` to close.

---

## Step 5: Create Tables (Database Schema)

You have two options:

### Option A: Using Python Script
Create a file `init_db.py`:

```python
from app.config.db import Base, engine
from app.models import (
    user_model,
    role_model,
    department_model,
    ticket_model,
    staff_model,
    notification_model,
    positions_model,
    telegram_model,
    status_model
)

# Create all tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
```

Then run via SSH:
```bash
python3 init_db.py
```

### Option B: Using SQL Dump
If you have an existing database dump:
```bash
mysql -u username_dbuser -p -h localhost username_support_system < backup.sql
```

---

## Step 6: Verify Connection in App

Your `db.py` configuration is already correct:
```python
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

The app will automatically read from `.env` file.

---

## Common Issues & Fixes

### Issue 1: "Connection refused"
- ✅ Ensure DB_HOST is `localhost` (not 127.0.0.1)
- ✅ Check if MySQL user has correct password
- ✅ Verify database user is added to the database

### Issue 2: "Access denied for user"
- ✅ Go to cPanel → MySQL Users → Check privileges
- ✅ Ensure user has SELECT, INSERT, UPDATE, DELETE permissions
- ✅ Click "Check Privileges" button

### Issue 3: "Unknown database"
- ✅ Verify database name matches exactly (case-sensitive)
- ✅ Check database prefix in cPanel (usually `username_dbname`)

### Issue 4: "pymysql not installed"
```bash
pip install --user pymysql
```

---

## Step 7: Secure Your .env File

```bash
# Via SSH, set proper permissions
chmod 600 .env

# Ensure .env is in .gitignore (if using Git)
echo ".env" >> .gitignore
```

---

## Step 8: Restart Passenger App

In cPanel:
1. Go to **Setup Python App**
2. Find your app
3. Click **Restart**

Your app will now use the cPanel database!

---

## Connection String Format

Your app builds the connection string like this:
```
mysql+pymysql://username_dbuser:password@localhost:3306/username_support_system
```

All values come from your `.env` file.

