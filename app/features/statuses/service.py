from typing import List

from sqlalchemy.orm import Session

from app.features.statuses.category_schema import Category
from app.features.statuses.priority_schema import Priority
from app.features.statuses.schema import Status


class StatusService:
    @staticmethod
    def getAllStatus(db: Session) -> List[Status]:
        return db.query(Status).filter(Status.id.in_([3, 4, 5, 6, 7])).all()

    @staticmethod
    def getAllCategory(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def getAllPriority(db: Session) -> List[Priority]:
        return db.query(Priority).all()

    @staticmethod
    def getPriorityById(db: Session, priority_id: int):
        return db.query(Priority).filter(Priority.id == priority_id).first()
