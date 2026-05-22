from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.positions.controller import PositionController
from app.features.positions.models import PositionRequest, PositionResponse
from app.middlewares.auth_middlewares import get_current_user, require_permission

router = APIRouter(prefix="/api/positions", tags=["positions"])


@router.get("", response_model=list[PositionResponse])
def getAllPositions(db: Session = Depends(get_db)):
    return PositionController.get_all(db)


@router.post("", response_model=PositionResponse)
def create_position(
    data: PositionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return PositionController.create(data, db, current_user, background_tasks)


@router.put("/{position_id}", response_model=PositionResponse)
def update_position(
    position_id: int,
    data: PositionRequest,
    db: Session = Depends(get_db),
):
    return PositionController.update(position_id, data, db)


@router.delete("/{position_id}")
def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("delete_position")),
):
    return PositionController.delete(position_id, db)
