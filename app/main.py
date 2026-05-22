import logging
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.db import Base, engine
from app.config.settings import get_settings
from app.features.registry import include_feature_routers, import_database_models
from app.middlewares.auth_middlewares import get_current_user

load_dotenv()
settings = get_settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=settings.cors_allow_credentials and "*" not in settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_feature_routers(app)

upload_dir = Path(settings.upload_dir)
upload_dir.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(upload_dir)),
    name="uploads",
)

app.mount(
    "/api/uploads",
    StaticFiles(directory=str(upload_dir)),
    name="api_uploads",
)


@app.on_event("startup")
def on_startup():
    import_database_models()

    logger.info("Registered tables: %s", list(Base.metadata.tables.keys()))
    if settings.create_tables_on_startup:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    else:
        logger.info("Automatic table creation is disabled.")


@app.get("/")
def root():
    return {"message": "API running", "service": settings.app_name}


@app.get("/me")
def whoami(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {"user": current_user}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}
