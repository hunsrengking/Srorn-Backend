from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.schema.student_schema import Student


class StudentService:

    @staticmethod
    def create_student(student_data, db):
        try:
            new_student = Student(**student_data.dict())

            db.add(new_student)
            db.commit()
            db.refresh(new_student)

            return new_student

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def get_all_students(db):
        try:
            students = db.query(Student).all()
            return students

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def get_student_by_id(student_id, db):
        try:
            student = db.query(Student).filter(Student.id == student_id).first()

            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            return student

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def update_student(student_id, student_data, db):
        try:
            student = db.query(Student).filter(Student.id == student_id).first()

            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            for key, value in student_data.dict(exclude_unset=True).items():
                setattr(student, key, value)

            db.commit()
            db.refresh(student)

            return student

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
