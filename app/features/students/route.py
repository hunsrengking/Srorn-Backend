from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.features.students.controller import StudentController
from app.features.students.models import StudentCreate, StudentResponse, StudentUpdate
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return StudentController.create(student, db, current_user, background_tasks)


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

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.delete(student_id, db)