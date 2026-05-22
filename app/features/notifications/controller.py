from sqlalchemy.orm import Session

from app.features.notifications.service import NotificationService
from app.features.users.schema import User


class NotificationController:
    @staticmethod
    def list_notifications(db: Session, current_user: User):
        return NotificationService.getUserNotifications(db, current_user.id)  # type: ignore

    @staticmethod
    def unread_count(db: Session, current_user: User):
        return {"count": NotificationService.getUnreadCount(db, current_user.id)}  # type: ignore

    @staticmethod
    def mark_as_read(notification_id: int, db: Session, current_user: User):
        NotificationService.markAsRead(db, notification_id, current_user.id)  # type: ignore
        return {"message": "Notification marked as read"}
