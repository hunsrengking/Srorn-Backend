from app.features.setting.code.service import CodeService


class CodeController:

    # code
    @staticmethod
    def getAllCode(db):
        return CodeService.getAllCode(db)

    @staticmethod
    def getCodeById(code_id, db):
        return CodeService.getCodeById(code_id, db)

    @staticmethod
    def createCode(code_data, db):
        return CodeService.createCode(code_data, db)

    @staticmethod
    def updateCode(code_id, code_data, db):
        return CodeService.updateCode(code_id, code_data, db)

    @staticmethod
    def disableCode(code_id, db):
        return CodeService.disableCode(code_id, db)

    @staticmethod
    def enableCode(code_id, db):
        return CodeService.enableCode(code_id, db)

    # codevalue
    @staticmethod
    def getAllCodeValue(db):
        return CodeService.getAllCodeValue(db)

    @staticmethod
    def getCodeValueByCode(code_name, db):
        return CodeService.getCodeValueByCode(code_name, db)

    @staticmethod
    def getCodeValueById(code_value_id, db):
        return CodeService.getCodeValueById(code_value_id, db)

    @staticmethod
    def createCodeValue(code_value_data, db):
        return CodeService.createCodeValue(code_value_data, db)

    @staticmethod
    def updateCodeValue(code_value_id, code_value_data, db):
        return CodeService.updateCodeValue(code_value_id, code_value_data, db)

    @staticmethod
    def disableCodeValue(code_value_id, db):
        return CodeService.disableCodeValue(code_value_id, db)

    @staticmethod
    def enableCodeValue(code_value_id, db):
        return CodeService.enableCodeValue(code_value_id, db)
