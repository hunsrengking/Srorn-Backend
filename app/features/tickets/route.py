from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.tickets.controller import TicketController
from app.features.tickets.models import TicketCreateReq, TicketResp, TicketUpdateReq
from app.features.users.schema import User
from app.middlewares.auth_middlewares import get_current_user, require_permission

router = APIRouter(prefix="/api/ticket", tags=["tickets"])


@router.get("")
def ListAllTicket(db: Session = Depends(get_db)):
    return TicketController.get_all(db)


@router.get("/status/waitingapprove")
def getTicketByStatus(db: Session = Depends(get_db)):
    return TicketController.get_waiting_approval(db)


@router.get("/file/download")
def download_ticket_file(path: str):
    return TicketController.download_file(path)


@router.get("/{id}")
def getTicketById(id: int, db: Session = Depends(get_db)):
    return TicketController.get_by_id(id, db)


@router.post("", response_model=TicketResp)
def CreateTicket(
    data: TicketCreateReq,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TicketController.create(data, background_tasks, db, current_user)


@router.patch("/{ticket_id}", response_model=TicketResp)
def UpdateTicket(
    ticket_id: int,
    data: TicketUpdateReq,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TicketController.update(ticket_id, data, background_tasks, db, current_user)


@router.patch("/{id}/approve")
def ApproveTicket(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TicketController.approve(id, db, current_user)


@router.patch("/{id}/reject")
def RejectTicket(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TicketController.reject(id, db, current_user)


@router.delete("/{id}")
def DeleteTicket(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("delete_ticket")),
):
    return TicketController.delete(id, db, current_user)


@router.post("/upload")
def upload_ticket_file(
    image: UploadFile | None = File(None),
    file: UploadFile | None = File(None),
):
    return TicketController.upload_file(image, file)
