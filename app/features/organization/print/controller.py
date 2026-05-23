from app.features.organization.print.service import OrganizationService


class OrganizationController:

    @staticmethod
    def getAllPrintCardTemplate(db):
        return OrganizationService.getAllPrintCardTemplate(db)

    @staticmethod
    def getPrintCardStudentTemplate(entity_id, db):
        return OrganizationService.getPrintCardStudentTemplate(entity_id, db)

    @staticmethod
    def getPrintCardStaffTemplate(entity_id, db):
        return OrganizationService.getPrintCardStaffTemplate(entity_id, db)

    @staticmethod
    def getAllPrintCard(db, entry_id=None, entity_type=None):
        return OrganizationService.getAllPrintCard(
            db, entry_id=entry_id, entity_type=entity_type # type: ignore
        )

    @staticmethod
    def getAllPrintCardById(print_card_id, db):
        return OrganizationService.getAllPrintCardById(print_card_id, db)

    @staticmethod
    def PrintCardNew(print_card_data, db, current_user, background_tasks):
        return OrganizationService.PrintCardNew(
            print_card_data, db, current_user, background_tasks
        )

    @staticmethod
    def UpdatePrintCard(
        print_card_id, print_card_data, db, current_user, background_tasks
    ):
        return OrganizationService.UpdatePrintCard(
            print_card_id, print_card_data, db, current_user, background_tasks
        )
