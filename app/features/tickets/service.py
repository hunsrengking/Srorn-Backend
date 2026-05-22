from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased

from app.config.iconfig import FRONTEND_URL
from app.constants.status_constants import *
from app.features.departments.service import DepartmentService
from app.features.notifications.models import NotificationRequest
from app.features.notifications.service import NotificationService
from app.features.statuses.category_schema import Category
from app.features.statuses.priority_schema import Priority
from app.features.statuses.schema import Status
from app.features.statuses.service import StatusService
from app.features.telegram.service import TelegramService
from app.features.tickets.item_schema import Item
from app.features.tickets.models import TicketRequest
from app.features.tickets.schema import Ticket
from app.features.users.schema import User
from app.features.users.service import UserService


class TicketService:
    @staticmethod
    def getAllTicket(db: Session) -> List[Dict[str, Any]]:
        rows = (
            db.query(
                Ticket.id.label("id"),
                Ticket.title.label("title"),
                Status.name.label("status"),
                Priority.name.label("priority"),
                Category.name.label("category"),
                Ticket.create_date.label("create_date"),
                Ticket.start_date.label("start_date"),
                Ticket.end_date.label("end_date"),
                User.username.label("assigned_to"),
            )
            .join(User, Ticket.assigned_to_id == User.id, isouter=True)
            .join(Status, Ticket.status_id == Status.id, isouter=True)
            .join(Priority, Ticket.priority_id == Priority.id, isouter=True)
            .join(Category, Ticket.category_id == Category.id, isouter=True)
            .filter(Ticket.status_id.in_([3, 4, 5, 6, 7]))
            .all()
        )

        tickets = [dict(row._mapping) for row in rows]
        if not tickets:
            return []

        ticket_ids = [ticket["id"] for ticket in tickets]
        item_rows = (
            db.query(
                Item.ticket_id.label("ticket_id"),
                Item.image_path.label("image_path"),
                Item.file_path.label("file_path"),
                Item.description.label("description"),
                Item.id.label("id"),
            )
            .filter(Item.ticket_id.in_(ticket_ids))
            .all()
        )

        items_by_ticket = defaultdict(list)
        for row in item_rows:
            item = dict(row._mapping)
            ticket_id = item.pop("ticket_id")
            items_by_ticket[ticket_id].append(item)

        for ticket in tickets:
            ticket["items"] = items_by_ticket.get(ticket["id"], [])

        return tickets

    @staticmethod
    def getTicketById(db: Session, ticket_id: int):
        UserRequester = aliased(User)
        UserAssigned = aliased(User)
        row = (
            db.query(
                Ticket.id.label("id"),
                Ticket.title.label("subject"),
                Ticket.description.label("description"),
                Ticket.status_id.label("status_id"),
                Status.name.label("status"),
                Ticket.priority_id.label("priority_id"),
                Priority.name.label("priority"),
                Ticket.category_id.label("category_id"),
                Category.name.label("category"),
                Ticket.assigned_to_id.label("assigned_to_id"),
                UserAssigned.username.label("assigned_to"),
                Ticket.requester_id.label("requester_id"),
                UserRequester.username.label("created_by"),
                Ticket.assigned_to_department_id.label("assigned_to_department_id"),
                Ticket.start_date.label("start_date"),
                Ticket.end_date.label("end_date"),
                Ticket.create_date.label("created_at"),
                Ticket.approved_date.label("approved_date"),
                Ticket.approved_by_id.label("approved_by_id"),
            )
            .join(UserRequester, Ticket.requester_id == UserRequester.id, isouter=True)
            .join(UserAssigned, Ticket.assigned_to_id == UserAssigned.id, isouter=True)
            .join(Status, Ticket.status_id == Status.id, isouter=True)
            .join(Priority, Ticket.priority_id == Priority.id, isouter=True)
            .join(Category, Ticket.category_id == Category.id, isouter=True)
            .filter(Ticket.id == ticket_id)
            .first()
        )

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with id={ticket_id} not found",
            )

        ticket = dict(row._mapping)

        item_rows = (
            db.query(
                Item.id.label("id"),
                Item.image_path.label("image_path"),
                Item.file_path.label("file_path"),
                Item.description.label("description"),
            )
            .filter(Item.ticket_id == ticket_id)
            .all()
        )

        ticket["items"] = [dict(row._mapping) for row in item_rows]

        return ticket

    @staticmethod
    def getTicketByStautus(db: Session):
        UserRequester = aliased(User)
        UserAssigned = aliased(User)
        rows = (
            db.query(
                Ticket.id,
                Ticket.title,
                UserAssigned.username.label("assigned_to"),
                UserRequester.username.label("created_by"),
                Status.name.label("status"),
                Category.name.label("category"),
                Priority.name.label("priority"),
                Ticket.create_date.label("created_at"),
            )
            .join(UserRequester, Ticket.requester_id == UserRequester.id, isouter=True)
            .join(UserAssigned, Ticket.assigned_to_id == UserAssigned.id, isouter=True)
            .join(Status, Ticket.status_id == Status.id, isouter=True)
            .join(Priority, Ticket.priority_id == Priority.id, isouter=True)
            .join(Category, Ticket.category_id == Category.id, isouter=True)
            .filter(Ticket.status_id == 8)
            .all()
        )
        return [dict(row._mapping) for row in rows]

    @staticmethod
    def createTicket(
        db: Session,
        data: TicketRequest,
        user_id: int,
        background_tasks: BackgroundTasks | None = None,
    ):
        try:
            if not data.title:
                raise HTTPException(status_code=400, detail="Ticket title is required")

            ticket = Ticket(
                title=data.title,
                description=data.description,
                status_id=STATUS_WAITING_APPROVE,
                requester_id=user_id,
                priority_id=data.priority_id,
                category_id=data.category_id,
                assigned_to_id=data.assigned_to_id,
                assigned_to_department_id=data.assigned_to_department_id,
                start_date=data.start_date,
                end_date=data.end_date,
            )

            db.add(ticket)
            db.flush()

            image_path = None
            file_path = None
            description = None

            if data.items:
                for item in data.items:
                    if item.get("image_path"):
                        image_path = item["image_path"]
                    if item.get("file_path"):
                        file_path = item["file_path"]
                    if item.get("description"):
                        description = item["description"]
                db_item = Item(
                    ticket_id=ticket.id,
                    image_path=image_path,
                    file_path=file_path,
                    description=description or "Attachments",
                )
                db.add(db_item)

            db.commit()
            db.refresh(ticket)

            notify_user_id = (
                ticket.assigned_to_id
                if ticket.assigned_to_id  # type: ignore
                else ticket.requester_id
            )

            NotificationService.createNotification(
                db,
                NotificationRequest(
                    user_id=notify_user_id,  # type: ignore
                    title="New Ticket Created",
                    message=f"Ticket #{ticket.id} - {ticket.title}",
                    link=f"/ticket/views/{ticket.id}",
                    type="ticket",
                ),
            )

            config = TelegramService.getActiveTelegramConfig(db)
            if config and background_tasks:
                requester = UserService.getUserById(db, user_id)
                priority = StatusService.getPriorityById(db, ticket.priority_id)  # type: ignore
                department = DepartmentService.getDepartmentById(db, ticket.assigned_to_department_id)  # type: ignore
                department_name = department["name"] if department else "Not yet assigned"
                priority_name = priority.name if priority else "Not yet assigned"
                deadline = (
                    ticket.end_date.strftime("%d %b %Y")
                    if ticket.end_date  # type: ignore
                    else "Not yet assigned"
                )
                ticket_url = f"{FRONTEND_URL}/ticket/views/{ticket.id}"
                message = (
                    f"<b>| New ticket:</b> #{ticket.id}\n"
                    f"<b>| Subject:</b> {ticket.title}\n"
                    f"<b>| Customer Name:</b> {requester.username}\n\n"  # type: ignore
                    f"<b>Hello team,</b> we have created a new ticket and assigned it to the "
                    f"<b>{department_name}</b> department. Please check and respond.\n"
                    "==============================\n"
                    f"<b>Priority:</b> {priority_name}\n"
                    f"<b>Dateline:</b> {deadline}\n"
                    "==============================\n\n"
                    f'<a href="{ticket_url}">View Ticket</a>'
                )

                background_tasks.add_task(
                    TelegramService.SendTelegramMessageAsync,
                    config.bot_token,
                    config.chat_id,
                    message,
                )
            return ticket

        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while creating ticket: {str(exc)}",
            )

    @staticmethod
    def UpdateTicket(
        db: Session,
        ticket_id: int,
        data: TicketRequest,
        user_id: int,
        background_tasks: BackgroundTasks | None = None,
    ):
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")

            update_data = data.model_dump(exclude_unset=True)
            update_data.pop("items", None)

            for field, value in update_data.items():
                setattr(ticket, field, value)

            ticket.assigned_by_id = user_id  # type: ignore

            db.commit()
            db.refresh(ticket)

            notify_user_id = (
                ticket.assigned_to_id if ticket.assigned_to_id else ticket.requester_id  # type: ignore
            )

            NotificationService.createNotification(
                db,
                NotificationRequest(
                    user_id=notify_user_id,  # type: ignore
                    title="Ticket Updated",
                    message=f"Ticket #{ticket.id} has been updated",
                    link=f"/ticket/views/{ticket.id}",
                    type="ticket",
                ),
            )

            config = TelegramService.getActiveTelegramConfig(db)
            if config and background_tasks:
                updater = UserService.getUserById(db, user_id)
                priority = StatusService.getPriorityById(db, ticket.priority_id)  # type: ignore
                assigned_user = UserService.getUserById(db, ticket.assigned_to_id) if ticket.assigned_to_id else None  # type: ignore
                assigned_username = (
                    assigned_user.username if assigned_user else "Not assigned"
                )
                priority_name = priority.name if priority else "Not assigned"
                deadline = (
                    ticket.end_date.strftime("%d %b %Y")
                    if ticket.end_date  # type: ignore
                    else "Not assigned"
                )

                ticket_url = f"{FRONTEND_URL}/ticket/views/{ticket.id}"

                message = (
                    f"<b>Ticket Updated</b> #{ticket.id}\n"
                    f"<b>Subject:</b> {ticket.title}\n"
                    f"<b>Updated by:</b> {updater.username}\n\n"  # type: ignore
                    "<b>Hello team,</b>\n"
                    "The following ticket has been updated. Please review the latest details below:\n"
                    "==============================\n"
                    f"<b>Priority:</b> {priority_name}\n"
                    f"<b>Assigned To:</b> {assigned_username}\n"
                    f"<b>Deadline:</b> {deadline}\n"
                    "==============================\n\n"
                    f'<a href="{ticket_url}">View Ticket</a>'
                )

                background_tasks.add_task(
                    TelegramService.SendTelegramMessageAsync,
                    config.bot_token,
                    config.chat_id,
                    message,
                )

            return ticket

        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while updating ticket: {str(exc)}",
            )

    @staticmethod
    def ApproveTicket(id: int, db: Session, user_id: int):
        ticket = db.query(Ticket).filter(Ticket.id == id).first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket.status_id != STATUS_WAITING_APPROVE:  # type: ignore
            raise HTTPException(status_code=400, detail="Ticket not waiting approval")

        ticket.status_id = STATUS_OPEN  # type: ignore
        ticket.approved_by_id = user_id  # type: ignore
        ticket.approved_date = datetime.now()  # type: ignore

        db.commit()
        db.refresh(ticket)

        return {"message": "Ticket approved successfully", "ticket_id": id}

    @staticmethod
    def RejectTicket(id: int, db: Session, user_id: int):
        ticket = db.query(Ticket).filter(Ticket.id == id).first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket.status_id != STATUS_WAITING_APPROVE:  # type: ignore
            raise HTTPException(status_code=400, detail="Ticket not waiting approval")

        ticket.status_id = STATUS_REJECT  # type: ignore
        ticket.approved_by_id = user_id  # type: ignore
        ticket.approved_date = datetime.now()  # type: ignore

        db.commit()
        db.refresh(ticket)
        return {"message": "Ticket reject successfully", "ticket_id": id}

    @staticmethod
    def DeleteTicket(id: int, db: Session, user_id: int):
        ticket = db.query(Ticket).filter(Ticket.id == id).first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket.status_id != STATUS_WAITING_APPROVE:  # type: ignore
            raise HTTPException(status_code=400, detail="Ticket not waiting approval")

        ticket.status_id = STATUS_DELETE  # type: ignore
        ticket.approved_by_id = user_id  # type: ignore
        ticket.approved_date = datetime.now()  # type: ignore

        db.commit()
        db.refresh(ticket)
        return {"message": "Ticket delete successfully", "ticket_id": id}
