from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.features.assets.models import AssetRequest, AssetResponse, AssetsTemplate
from app.features.assets.controller import AssetController
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/assets", tags=["Assets"])


@router.get("/template", response_model=AssetsTemplate)
def getAssetsTemplate(
    db: Session = Depends(get_db),
):
    return AssetController.getAssetsTemplate(db)


@router.post("", response_model=AssetResponse)
def create_asset(
    asset: AssetRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetController.creates(asset, db)


@router.get("", response_model=list[AssetResponse])
def findAll(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetController.findAll(db)


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetController.findById(asset_id, db)


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset: AssetRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetController.updated(asset_id, asset, db)


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetController.deleted(asset_id, db)
