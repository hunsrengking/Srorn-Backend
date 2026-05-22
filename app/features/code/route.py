from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.features.code.controller import CodeController
from app.features.code.models import (
    CodeRequest,
    CodeResponse,
    CodeValueRequest,
    CodeValueResponse,
)

router = APIRouter(prefix="/api/code", tags=["Code"])


# code
@router.get("/", response_model=list[CodeResponse])
def getAllCode(
    db: Session = Depends(get_db),
):
    return CodeController.getAllCode(db)


@router.get("/id/{code_id}", response_model=CodeResponse)
def getCodeById(
    code_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.getCodeById(code_id, db)


@router.post("/", response_model=CodeResponse)
def createCode(
    code_data: CodeRequest,
    db: Session = Depends(get_db),
):
    return CodeController.createCode(code_data, db)


@router.put("/id/{code_id}", response_model=CodeResponse)
def updateCode(
    code_id: int,
    code_data: CodeRequest,
    db: Session = Depends(get_db),
):
    return CodeController.updateCode(code_id, code_data, db)


@router.delete("/id/{code_id}", response_model=CodeResponse)
def disableCode(
    code_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.disableCode(code_id, db)


@router.put("/id/{code_id}/enable", response_model=CodeResponse)
def enableCode(
    code_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.enableCode(code_id, db)


# codevalue
@router.get("/value/", response_model=list[CodeValueResponse])
def getAllCodeValue(
    db: Session = Depends(get_db),
):
    return CodeController.getAllCodeValue(db)


@router.get("/value/id/{code_value_id}", response_model=CodeValueResponse)
def getCodeValueById(
    code_value_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.getCodeValueById(code_value_id, db)


@router.get("/value/code/{code_name}", response_model=list[CodeValueResponse])
def getCodeValueByCode(
    code_name: str,
    db: Session = Depends(get_db),
):
    return CodeController.getCodeValueByCode(code_name, db)


@router.post("/value/", response_model=CodeValueResponse)
def createCodeValue(
    code_value_data: CodeValueRequest,
    db: Session = Depends(get_db),
):
    return CodeController.createCodeValue(code_value_data, db)


@router.put("/value/id/{code_value_id}", response_model=CodeValueResponse)
def updateCodeValue(
    code_value_id: int,
    code_value_data: CodeValueRequest,
    db: Session = Depends(get_db),
):
    return CodeController.updateCodeValue(code_value_id, code_value_data, db)


@router.delete("/value/id/{code_value_id}", response_model=CodeValueResponse)
def disableCodeValue(
    code_value_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.disableCodeValue(code_value_id, db)


@router.put("/value/id/{code_value_id}/enable", response_model=CodeValueResponse)
def enableCodeValue(
    code_value_id: int,
    db: Session = Depends(get_db),
):
    return CodeController.enableCodeValue(code_value_id, db)
