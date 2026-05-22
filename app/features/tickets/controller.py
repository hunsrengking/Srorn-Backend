import os
from urllib.parse import urlparse

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.config.cloudinary import upload_file_to_cloudinary, upload_image_to_cloudinary
from app.features.tickets.service import TicketService
from app.features.tickets.models import TicketRequest


class TicketController:
    @staticmethod
    def get_all(db: Session):
        return TicketService.getAllTicket(db)

    @staticmethod
    def get_by_id(ticket_id: int, db: Session):
        ticket = TicketService.getTicketById(db, ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=404,
                detail=f"Ticket with id={ticket_id} not found",
            )
        return ticket

    @staticmethod
    def get_waiting_approval(db: Session):
        return TicketService.getTicketByStautus(db)

    @staticmethod
    def create(data: TicketRequest, background_tasks, db: Session, current_user):
        return TicketService.createTicket(
            db=db,
            data=data,
            user_id=current_user.id,  # type: ignore
            background_tasks=background_tasks,  # type: ignore
        )  # type: ignore

    @staticmethod
    def update(
        ticket_id: int,
        data: TicketRequest,
        background_tasks,
        db: Session,
        current_user,
    ):
        return TicketService.UpdateTicket(
            db=db,
            ticket_id=ticket_id,
            data=data,
            user_id=current_user.id,  # type: ignore
            background_tasks=background_tasks,
        )

    @staticmethod
    def approve(ticket_id: int, db: Session, current_user):
        return TicketService.ApproveTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def reject(ticket_id: int, db: Session, current_user):
        return TicketService.RejectTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def delete(ticket_id: int, db: Session, current_user):
        return TicketService.DeleteTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def upload_file(image: UploadFile | None, file: UploadFile | None):
        result = {}

        if image:
            result["image_path"] = upload_image_to_cloudinary(image)

        if file:
            result["file_path"] = upload_file_to_cloudinary(file)

        return result

    @staticmethod
    def download_file(path: str):
        parsed_url = urlparse(path)
        if parsed_url.scheme in {"http", "https"}:
            return RedirectResponse(path)

        real_path = path.replace("app/", "")
        real_path = os.path.join("app", real_path)

        if not os.path.exists(real_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            real_path,
            filename=os.path.basename(real_path),
            media_type="application/octet-stream",
        )
