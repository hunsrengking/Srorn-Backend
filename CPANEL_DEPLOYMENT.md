# cPanel Deployment Guide

## Steps to Host on cPanel:

### 1. **Upload Project Files**
   - Upload all files to your cPanel public_html or a subdirectory
   - Ensure passenger_wsgi.py is in the root directory

### 2. **Create Python Application in cPanel**
   - Go to **cPanel → Setup Python App**
   - Select Python version (3.8 or higher recommended)
   - Set Application root to your project directory
   - Set Application startup file to `passenger_wsgi.py`
   - Set Application entry point to `application`
   - Set Passenger log file path (for debugging)

### 3. **Install Dependencies**
   - In cPanel Terminal or SSH:
   ```bash
   cd /home/username/public_html/your_app
   python3 -m pip install --user -r requirements.txt
   ```

### 4. **Configure Environment Variables**
   - Create a `.env` file in your project root with:
   ```
   DATABASE_URL=your_mysql_connection_string
   SECRET_KEY=your_secret_key
   ```
   - Set proper permissions: `chmod 600 .env`

### 5. **Set Proper Permissions**
   ```bash
   chmod 755 passenger_wsgi.py
   chmod 755 app/
   chmod 644 app/*.py
   ```

### 6. **Restart Application**
   - Click "Restart" in the Python App setup in cPanel

### 7. **Access Your Application**
   - Your API will be available at your domain URL
   - Example: `https://yourdomain.com/docs` for FastAPI docs

## Troubleshooting:

- Check **Passenger Error Log** in cPanel for errors
- Verify all imports in requirements.txt are installed
- Ensure database credentials are correct in `.env`
- Check file permissions if getting 403/404 errors
- Clear browser cache if getting stale responses

## Important Notes:

- `passenger_wsgi.py` must export an `application` variable
- Use `asgiref` to convert ASGI (FastAPI) to WSGI (Passenger)
- Keep `requirements.txt` updated with all dependencies
- Use `.env` for sensitive configuration, never hardcode credentials
