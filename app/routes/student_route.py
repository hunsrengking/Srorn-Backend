from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.controllers.student_controller import StudentController
from app.models.student_model import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return StudentController.create(student, db)


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return StudentController.get_all(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.get_by_id(student_id, db)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentUpdate, db: Session = Depends(get_db)
):
    return StudentController.update(student_id, student, db)
