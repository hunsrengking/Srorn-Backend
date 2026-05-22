# Srorn Backend

FastAPI backend for Srorn. The API is mounted under `/api` for application
routes, with `/api/health` available for health checks.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Update `.env` with the local MySQL connection before starting the server.

## Configuration

Important environment variables:

- `FRONTEND_URL`: public frontend URL used in notification links.
- `BACKEND_CORS_ORIGINS`: comma-separated browser origins allowed to call the API.
- `DATABASE_URL`: optional full SQLAlchemy URL. If omitted, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_NAME` are used.
- `CREATE_TABLES_ON_STARTUP`: set to `false` when schema management moves to migrations.
- `UPLOAD_DIR`: local upload directory served by `/uploads` and `/api/uploads`.

## Feature Layout

Each folder in `app/features` owns one business area.

```text
app/features/<feature>/
  route.py       FastAPI router and URL wiring
  controller.py  FeatureController class used by route.py
  service.py     Business logic and database work
  models.py      Pydantic request/response models
  schema.py      SQLAlchemy database model
```

Not every feature needs every file. Keep shared infrastructure in `app/config`,
`app/middlewares`, and `app/constants`.

To add a new feature:

1. Create `app/features/<feature>/`.
2. Put FastAPI decorators only in `route.py`.
3. Put request handling methods on `<Feature>Controller` in `controller.py`.
4. Add the files that feature needs.
5. Add its router module to `ROUTER_MODULES` in `app/features/registry.py`.
6. If it defines SQLAlchemy tables, add those modules to
   `DATABASE_MODEL_MODULES` in `app/features/registry.py`.
