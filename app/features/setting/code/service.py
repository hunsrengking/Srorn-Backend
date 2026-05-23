from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.features.setting.code.schema import Code, CodeValue


class CodeService:

    # Code
    @staticmethod
    def getAllCode(db):
        try:
            return db.query(Code).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getAllCodeWithStatusActive(db):
        try:
            return db.query(Code).filter(Code.is_active == True).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def createCode(code_data, db):
        try:
            new_code = Code(
                codes_name=code_data.codes_name,
                is_active=code_data.is_active,
            )
            db.add(new_code)
            db.commit()
            db.refresh(new_code)
            return new_code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getCodeById(code_id, db):
        try:
            code = (
                db.query(Code)
                .filter(Code.id == code_id)
                .first()
            )
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            return code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getCodeByName(code_name, db):
        try:
            code = (
                db.query(Code)
                .filter(Code.codes_name == code_name, Code.is_active == True)
                .first()
            )
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            return code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def updateCode(code_id, code_data, db):
        try:
            code = CodeService.getCodeById(code_id, db)
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            code.codes_name = code_data.codes_name
            code.is_active = code_data.is_active
            db.commit()
            db.refresh(code)
            return code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def disableCode(code_id, db):
        try:
            code = CodeService.getCodeById(code_id, db)
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            code.is_active = False
            db.commit()
            db.refresh(code)
            return code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def enableCode(code_id, db):
        try:
            code = CodeService.getCodeById(code_id, db)
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            code.is_active = True
            db.commit()
            db.refresh(code)
            return code
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    # CodeValue
    @staticmethod
    def getAllCodeValue(db):
        try:
            return db.query(CodeValue).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getAllCodeValueWithStatusActive(db):
        try:
            return db.query(CodeValue).filter(CodeValue.is_active == True).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getCodeValueByCode(code_name, db):
        try:
            code = CodeService.getCodeByName(code_name, db)
            return (
                db.query(CodeValue)
                .filter(CodeValue.code_id == code.id, CodeValue.is_active == True)
                .order_by(CodeValue.order_position)
                .all()
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def getCodeValueById(code_value_id, db):
        try:
            code_value = (
                db.query(CodeValue).filter(CodeValue.id == code_value_id).first()
            )
            if not code_value:
                raise HTTPException(status_code=404, detail="CodeValue not found")
            return code_value
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def createCodeValue(code_value_data, db):
        try:
            code = CodeService.getCodeById(code_value_data.code_id, db)
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            new_code_value = CodeValue(
                code_id=code_value_data.code_id,
                code_value=code_value_data.code_value,
                code_description=code_value_data.code_description,
                order_position=code_value_data.order_position,
                is_active=code_value_data.is_active,
            )
            db.add(new_code_value)
            db.commit()
            db.refresh(new_code_value)
            return new_code_value
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def updateCodeValue(code_value_id, code_value_data, db):
        try:
            code_value = CodeService.getCodeValueById(code_value_id, db)
            if not code_value:
                raise HTTPException(status_code=404, detail="CodeValue not found")
            code = CodeService.getCodeById(code_value_data.code_id, db)
            if not code:
                raise HTTPException(status_code=404, detail="Code not found")
            code_value.code_id = code_value_data.code_id
            code_value.code_value = code_value_data.code_value
            code_value.code_description = code_value_data.code_description
            code_value.order_position = code_value_data.order_position
            code_value.is_active = code_value_data.is_active
            db.commit()
            db.refresh(code_value)
            return code_value
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def disableCodeValue(code_value_id, db):
        try:
            code_value = CodeService.getCodeValueById(code_value_id, db)
            if not code_value:
                raise HTTPException(status_code=404, detail="CodeValue not found")
            code_value.is_active = False
            db.commit()
            db.refresh(code_value)
            return code_value
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def enableCodeValue(code_value_id, db):
        try:
            code_value = CodeService.getCodeValueById(code_value_id, db)
            if not code_value:
                raise HTTPException(status_code=404, detail="CodeValue not found")
            code_value.is_active = True
            db.commit()
            db.refresh(code_value)
            return code_value
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
