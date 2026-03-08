from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.controllers.student_controller import StudentController
from app.models.student_model import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/api", tags=["Students"])


@router.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return StudentController.create(student, db)


@router.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return StudentController.get_all(db)


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.get_by_id(student_id, db)


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentUpdate, db: Session = Depends(get_db)
):
    return StudentController.update(student_id, student, db)

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.delete(student_id, db)