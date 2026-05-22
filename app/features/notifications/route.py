from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.notifications.controller import NotificationController
from app.features.notifications.models import NotificationResponse
from app.features.users.schema import User
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
def listNotifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NotificationController.list_notifications(db, current_user)


@router.get("/unread-count")
def unreadCount(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NotificationController.unread_count(db, current_user)


@router.put("/{notification_id}/read")
def readNotification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NotificationController.mark_as_read(notification_id, db, current_user)
