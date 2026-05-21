import os
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.db import Base, engine
from app.features.registry import include_feature_routers, import_database_models
from app.middlewares.auth_middlewares import get_current_user

load_dotenv()
app = FastAPI(title="MyApi with Roles & Permissions")

# origin = [
#     "http://localhost:5173",
#     "http://192.168.100.151:5173",
#     "https://wupai.smartdigitalhr.com",
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origin,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_feature_routers(app)

if not os.path.exists("public/uploads"):
    os.makedirs("public/uploads")

app.mount(
    "/uploads",
    StaticFiles(directory="public/uploads"),
    name="uploads",
)


@app.on_event("startup")
def on_startup():
    import_database_models()

    print("Registered tables before create_all():", list(Base.metadata.tables.keys()))

    # Now create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified.")


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/me")
def whoami(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {"user": current_user}


@app.get("/api/health")
def health():
    return {"status": "ok"}
