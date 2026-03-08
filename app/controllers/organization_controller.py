from app.services.organization_service import OrganizationService

class OrganizationController:

    @staticmethod
    def getAllPrintCard(db):
        return OrganizationService.getAllPrintCard(db)

    @staticmethod
    def getAllPrintCardById(print_card_id, db):
        return OrganizationService.getAllPrintCardById(print_card_id, db)

    @staticmethod
    def PrintCardNew(print_card_data, db):
        return OrganizationService.PrintCardNew(print_card_data, db)