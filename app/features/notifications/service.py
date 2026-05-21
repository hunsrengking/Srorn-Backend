from sqlalchemy.orm import Session
from app.features.notifications.schema import Notification
from app.features.notifications.models import NotificationCreate
from fastapi import BackgroundTasks
from app.features.telegram import service as telegram_service
from app.config.iconfig import FRONTEND_URL


def createNotification(db: Session, data: NotificationCreate):
    notification = Notification(**data.dict())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def getUserNotifications(db: Session, user_id: int, limit: int = 10):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .all()
    )


def getUnreadCount(db: Session, user_id: int):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.is_read == False)
        .count()
    )


def markAsRead(db: Session, notification_id: int, user_id: int):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )

    if notification:
        notification.is_read = True # type: ignore
        db.commit()

    return notification


def notify_action(
    db: Session,
    user,
    title: str,
    message: str,
    link: str,
    notification_type: str,
    background_tasks: BackgroundTasks | None = None,
    telegram_message: str | None = None,
):
    """
    Standard function to create an internal notification and optionally send a Telegram message.
    """
    # 1. Internal Notification
    createNotification(
        db,
        NotificationCreate(
            user_id=user.id,
            title=title,
            message=message,
            link=link,
            type=notification_type,
        ),
    )

    # 2. Telegram Notification
    if telegram_message and background_tasks:
        config = telegram_service.getActiveTelegramConfig(db)
        if config:
            background_tasks.add_task(
                telegram_service.SendTelegramMessageAsync,
                config.bot_token,
                config.chat_id,
                telegram_message,
            )
