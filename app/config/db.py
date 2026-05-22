from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import get_settings


settings = get_settings()

if settings.missing_database_values:
    missing = ", ".join(settings.missing_database_values)
    raise RuntimeError(f"Missing database configuration: {missing}")

DATABASE_URL = settings.database_url or URL.create(
    drivername="mysql+pymysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=int(settings.db_port),
    database=settings.db_name,
)

engine = create_engine(DATABASE_URL, echo=settings.db_echo, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
