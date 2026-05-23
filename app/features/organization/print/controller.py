from app.features.organization.print.service import PrintCardService


class PrintCardController:

    @staticmethod
    def getPrintCardStudentTemplate(entity_id, db):
        return PrintCardService.getPrintCardStudentTemplate(entity_id, db)

    @staticmethod
    def getPrintCardData(db):
        return PrintCardService.getPrintCardData(db)

    @staticmethod
    def getPrintCardStaffTemplate(entity_id, db):
        return PrintCardService.getPrintCardStaffTemplate(entity_id, db)

    @staticmethod
    def getPrintCardById(print_card_id, db):
        return PrintCardService.getPrintCardById(print_card_id, db)

    @staticmethod
    def getPrintCardByEntityId(entity_id, db):
        return PrintCardService.getPrintCardByEntityId(entity_id, db)

    @staticmethod
    def PrintCardNew(print_card_data, db, current_user, background_tasks):
        return PrintCardService.PrintCardNew(
            print_card_data, db, current_user, background_tasks
        )

    @staticmethod
    def UpdatePrintCard(
        print_card_id, print_card_data, db, current_user, background_tasks
    ):
        return PrintCardService.UpdatePrintCard(
            print_card_id, print_card_data, db, current_user, background_tasks
        )
