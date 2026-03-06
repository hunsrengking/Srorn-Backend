from app.services.student_service import StudentService


class StudentController:

    @staticmethod
    def create(student_data, db):
        return StudentService.create_student(student_data, db)

    @staticmethod
    def get_all(db):
        return StudentService.get_all_students(db)

    @staticmethod
    def get_by_id(student_id, db):
        return StudentService.get_student_by_id(student_id, db)

    @staticmethod
    def update(student_id, student_data, db):
        return StudentService.update_student(student_id, student_data, db)
