from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, BackgroundTasks
from app.features.positions.schema import Position
from app.features.students.schema import Student
from app.features.notifications.service import notify_action


class StudentService:

    @staticmethod
    def create_student(student_data, db, current_user=None, background_tasks: BackgroundTasks | None = None):
        try:
            data = student_data.dict()

            # auto generate display_name
            firstname = data.get("firstname", "")
            lastname = data.get("lastname", "")
            data["display_name"] = f"{firstname} {lastname}".strip()

            new_student = Student(**data)

            db.add(new_student)
            db.commit()
            db.refresh(new_student)

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>🎓 New Student Created:</b> {new_student.display_name}\n"
                    f"<b>👤 Created by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                notify_action(
                    db=db,
                    user=current_user,
                    title="New Student Created",
                    message=f"Student {new_student.display_name} has been added",
                    link=f"/students/views/{new_student.id}",
                    notification_type="student",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return new_student

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def get_all_students(db):
        try:
            students = (
                db.query(
                    Student.id,
                    Student.firstname,
                    Student.lastname,
                    Student.khmer_firstname,
                    Student.khmer_lastname,
                    Student.display_name,
                    Student.position_id,
                    Student.is_active,
                    Student.created_at,
                    Student.updated_at,
                    Student.is_deleted,
                    Position.title.label("position_name")
                )
                .join(Position, Student.position_id == Position.id)
                .filter(Student.is_deleted == False)
                .all()
            )

            return [dict(row._mapping) for row in students]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def get_student_by_id(student_id, db):
        try:
            student = (
                db.query(
                    Student.id,
                    Student.firstname,
                    Student.lastname,
                    Student.khmer_firstname,
                    Student.khmer_lastname,
                    Student.display_name,
                    Student.position_id,
                    Student.is_active,
                    Student.created_at,
                    Student.updated_at,
                    Student.is_deleted,
                    Position.title.label("position_name")
                )
                .join(Position, Student.position_id == Position.id)
                .filter(
                    Student.id == student_id,
                    Student.is_deleted == False
                )
                .first()
            )

            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            return dict(student._mapping)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def update_student(student_id, student_data, db):
        try:
            student = db.query(Student).filter(Student.id == student_id).first()

            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            update_data = student_data.model_dump(exclude_unset=True)
            
            # auto generate display_name
            firstname = update_data.get("firstname", student.firstname)
            lastname = update_data.get("lastname", student.lastname)
            update_data["display_name"] = f"{firstname} {lastname}"

            for key, value in update_data.items():
                setattr(student, key, value)

            db.commit()
            db.refresh(student)

            return student

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    @staticmethod
    def delete_student(student_id, db):
        try:
            student = db.query(Student).filter(Student.id == student_id).first()

            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            student.is_deleted = True
            db.commit()
            return student

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
