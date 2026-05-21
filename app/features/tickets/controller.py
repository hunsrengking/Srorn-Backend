import os
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.features.tickets import service as ticket_service
from app.features.tickets.models import TicketCreateReq, TicketUpdateReq

UPLOAD_IMAGE_DIR = "app/uploads/tickets/images"
UPLOAD_FILE_DIR = "app/uploads/tickets/files"


class TicketController:
    @staticmethod
    def get_all(db: Session):
        return ticket_service.getAllTicket(db)

    @staticmethod
    def get_by_id(ticket_id: int, db: Session):
        ticket = ticket_service.getTicketById(db, ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=404,
                detail=f"Ticket with id={ticket_id} not found",
            )
        return ticket

    @staticmethod
    def get_waiting_approval(db: Session):
        return ticket_service.getTicketByStautus(db)

    @staticmethod
    def create(data: TicketCreateReq, background_tasks, db: Session, current_user):
        return ticket_service.createTicket(
            db=db,
            data=data,
            user_id=current_user.id,  # type: ignore
            background_tasks=background_tasks,  # type: ignore
        )  # type: ignore

    @staticmethod
    def update(
        ticket_id: int,
        data: TicketUpdateReq,
        background_tasks,
        db: Session,
        current_user,
    ):
        return ticket_service.UpdateTicket(
            db=db,
            ticket_id=ticket_id,
            data=data,
            user_id=current_user.id,  # type: ignore
            background_tasks=background_tasks,
        )

    @staticmethod
    def approve(ticket_id: int, db: Session, current_user):
        return ticket_service.ApproveTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def reject(ticket_id: int, db: Session, current_user):
        return ticket_service.RejectTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def delete(ticket_id: int, db: Session, current_user):
        return ticket_service.DeleteTicket(
            id=ticket_id,
            db=db,
            user_id=current_user.id,  # type: ignore
        )

    @staticmethod
    def upload_file(image: UploadFile | None, file: UploadFile | None):
        os.makedirs(UPLOAD_IMAGE_DIR, exist_ok=True)
        os.makedirs(UPLOAD_FILE_DIR, exist_ok=True)

        result = {}

        if image:
            ext = image.filename.split(".")[-1]  # type: ignore
            image_name = f"{uuid.uuid4()}.{ext}"
            image_path = f"{UPLOAD_IMAGE_DIR}/{image_name}"

            with open(image_path, "wb") as output:
                output.write(image.file.read())

            result["image_path"] = image_path

        if file:
            ext = file.filename.split(".")[-1]  # type: ignore
            file_name = f"{uuid.uuid4()}.{ext}"
            file_path = f"{UPLOAD_FILE_DIR}/{file_name}"

            with open(file_path, "wb") as output:
                output.write(file.file.read())

            result["file_path"] = file_path

        return result

    @staticmethod
    def download_file(path: str):
        real_path = path.replace("app/", "")
        real_path = os.path.join("app", real_path)

        if not os.path.exists(real_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            real_path,
            filename=os.path.basename(real_path),
            media_type="application/octet-stream",
        )
