from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.features.notifications.models import NotificationRequest
from app.features.notifications.schema import Notification
from app.features.setting.telegram.service import TelegramService


class NotificationService:
    @staticmethod
    def createNotification(db: Session, data: NotificationRequest):
        notification = Notification(**data.model_dump())
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def getUserNotifications(db: Session, user_id: int, limit: int = 10):
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def getUnreadCount(db: Session, user_id: int):
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .count()
        )

    @staticmethod
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
            notification.is_read = True  # type: ignore
            db.commit()

        return notification

    @staticmethod
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
        NotificationService.createNotification(
            db,
            NotificationRequest(
                user_id=user.id,
                title=title,
                message=message,
                link=link,
                type=notification_type,
            ),
        )

        if telegram_message and background_tasks:
            config = TelegramService.getActiveTelegramConfig(db)
            if config:
                background_tasks.add_task(
                    TelegramService.SendTelegramMessageAsync,
                    config.bot_token,
                    config.chat_id,
                    telegram_message,
                )
