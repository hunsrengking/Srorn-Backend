import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_bool(name: str, default: bool = False) -> bool:
    value = _env(name)
    if not value:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _csv(value: str) -> Tuple[str, ...]:
    return tuple(item.strip().rstrip("/") for item in value.split(",") if item.strip())


def _default_cors_origins(frontend_url: str) -> Tuple[str, ...]:
    origins = {
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    }
    if frontend_url:
        origins.add(frontend_url.rstrip("/"))
    return tuple(sorted(origins))


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    log_level: str
    frontend_url: str
    cors_origins: Tuple[str, ...]
    cors_allow_credentials: bool
    upload_dir: str
    database_url: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    db_echo: bool
    create_tables_on_startup: bool

    @property
    def missing_database_values(self) -> Tuple[str, ...]:
        if self.database_url:
            return ()

        required = {
            "DB_USER": self.db_user,
            "DB_PASSWORD": self.db_password,
            "DB_HOST": self.db_host,
            "DB_PORT": self.db_port,
            "DB_NAME": self.db_name,
        }
        return tuple(name for name, value in required.items() if not value)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    frontend_url = _env("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    cors_origins = _csv(_env("BACKEND_CORS_ORIGINS") or _env("CORS_ORIGINS"))

    return Settings(
        app_name=_env("APP_NAME", "Srorn API"),
        app_env=_env("APP_ENV", "development"),
        log_level=_env("LOG_LEVEL", "INFO").upper(),
        frontend_url=frontend_url,
        cors_origins=cors_origins or _default_cors_origins(frontend_url),
        cors_allow_credentials=_env_bool("CORS_ALLOW_CREDENTIALS", True),
        upload_dir=_env("UPLOAD_DIR", "public/uploads"),
        database_url=_env("DATABASE_URL"),
        db_user=_env("DB_USER"),
        db_password=_env("DB_PASSWORD"),
        db_host=_env("DB_HOST"),
        db_port=_env("DB_PORT"),
        db_name=_env("DB_NAME"),
        db_echo=_env_bool("DB_ECHO", False),
        create_tables_on_startup=_env_bool("CREATE_TABLES_ON_STARTUP", True),
    )
