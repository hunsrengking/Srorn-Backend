from app.features.organization.service import OrganizationService

class OrganizationController:

    @staticmethod
    def getAllPrintCardTemplate(db):
        return OrganizationService.getAllPrintCardTemplate(db)

    @staticmethod
    def getAllPrintCard(db):
        return OrganizationService.getAllPrintCard(db)

    @staticmethod
    def getAllPrintCardById(print_card_id, db):
        return OrganizationService.getAllPrintCardById(print_card_id, db)

    @staticmethod
    def PrintCardNew(print_card_data, db, current_user, background_tasks):
        return OrganizationService.PrintCardNew(print_card_data, db, current_user, background_tasks)

    @staticmethod
    def UpdatePrintCard(print_card_id, print_card_data, db, current_user, background_tasks):
        return OrganizationService.UpdatePrintCard(print_card_id, print_card_data, db, current_user, background_tasks)