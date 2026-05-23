from app.features.organization.offices.service import OfficeService

class OfficeController:

    @staticmethod
    def creates(office_data, db, current_user, background_tasks):
        return OfficeService.created(office_data, db, current_user, background_tasks)

    @staticmethod
    def findAll(db):
        return OfficeService.findAll(db)

    @staticmethod
    def findById(office_id, db):
        return OfficeService.findById(office_id, db)

    @staticmethod
    def updated(office_id, office_data, db, current_user, background_tasks):
        return OfficeService.update(office_id, office_data, db, current_user, background_tasks)

    @staticmethod
    def deleted(office_id, db, current_user, background_tasks):
        return OfficeService.deleted(office_id, db, current_user, background_tasks)