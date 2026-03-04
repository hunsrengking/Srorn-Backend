# Srorn (Dockerized)

This repository contains the backend (`Srorn-Backend`) and frontend (`Srorn-Frontend`). The included `docker-compose.yml` builds and runs:

- `db` (optional MySQL)
- `backend` (FastAPI uvicorn)
- `frontend` (Vite build served by Nginx)

Quick start (from the repository root):

```bash
# Build and run everything in detached mode
docker compose up --build -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

**Access from other devices on the network:**

Your frontend automatically proxies API calls through nginx, so it works seamlessly:
- **Frontend:** `http://<YOUR_MACHINE_IP>:3000/login`
- Direct Backend API (if needed): `http://<YOUR_MACHINE_IP>:8000/api/...`
- Database: `<YOUR_MACHINE_IP>:3306`

**Find your machine IP:**
- **Windows:** Open Command Prompt and run `ipconfig`, look for IPv4 Address (usually `192.168.x.x` or `10.x.x.x`)
- **Linux/Mac:** Run `ifconfig` or `ip addr show`

**Troubleshooting network access:**
1. Ensure firewall allows ports `3000`, `8000`, `3306` (or adjust docker-compose.yml)
2. Both machines must be on the same network
3. Check logs with: `docker compose logs -f`
4. Verify backend is accessible: `curl -I http://YOUR_IP:8000/api/health`

Environment: The compose file sets DB credentials for `db` and passes them to the backend. If you prefer to use a host database, update `docker-compose.yml` or provide env vars.

Simple daily workflow:

- Development Machine: Code → `git add` → `git commit` → `git push`
- Production Server: `git pull` → `docker compose up --build -d`

Files added:

- `docker-compose.yml` (root)
- `Srorn-Backend/Dockerfile`
- `Srorn-Frontend/Dockerfile`
- `Srorn-Frontend/nginx.conf`

Next steps:

- If you want persistent `.env` handling, move credentials into an `.env` and reference it from the compose file.
- Optionally run `docker compose up --build` locally to verify.

- Final Daily Workflow After Merge
-- Developer Side
git add .
git commit -m "New feature"
git push

-- Production Server
cd frontend
git pull

cd backend
git pull

cd System
git pull
docker compose down
docker compose up --build -d

Structue Project Run Build in Docker

System/
    frontend/
    backend/
.env.example
docker-compose.yml
README.md