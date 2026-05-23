from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.features.assets.schema import Asset
from app.features.setting.code.service import CodeService
from app.features.organization.offices.service import OfficeService
from app.features.organization.departments.service import DepartmentService
from app.features.assets.assignments_schema import AssetAssignment
from sqlalchemy.orm import joinedload
from app.features.assets.assignments_schema import AssetAssignment
from sqlalchemy.orm import joinedload


class AssetService:

    # Asset
    @staticmethod
    def getAssetsTemplate(db):
        try:
            assetTypeOptions = CodeService.getCodeValueByCode("AssetType", db)
            officeOptions = OfficeService.findAll(db)
            departmentOptions = DepartmentService.getAllDepartment(db)
            modelOptions = CodeService.getCodeValueByCode("ModelType", db)
            cpuOptions = CodeService.getCodeValueByCode("CPU", db)
            ramOptions = CodeService.getCodeValueByCode("RAM", db)
            hhdOptions = CodeService.getCodeValueByCode("HDD", db)
            osOptions = CodeService.getCodeValueByCode("OS", db)
            locationOptions = CodeService.getCodeValueByCode("Location", db)

            return {
                "assetTypeOptions": assetTypeOptions,
                "officeOptions": officeOptions,
                "departmentOptions": departmentOptions,
                "modelOptions": modelOptions,
                "cpuOptions": cpuOptions,
                "ramOptions": ramOptions,
                "hhdOptions": hhdOptions,
                "osOptions": osOptions,
                "locationOptions": locationOptions,
            }

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def findAll(db):
        try:

            assets = (
                db.query(Asset)
                .options(
                    joinedload(Asset.device_type),
                    joinedload(Asset.device_model),
                    joinedload(Asset.location),
                    joinedload(Asset.department),
                    joinedload(Asset.cpu),
                    joinedload(Asset.ram),
                    joinedload(Asset.hhd),
                    joinedload(Asset.os),
                    joinedload(Asset.office),
                )
                .all()
            )

            # Get active assignments
            assignments = (
                db.query(AssetAssignment)
                .filter(AssetAssignment.is_returned == False)
                .options(joinedload(AssetAssignment.staff))
                .all()
            )

            assignment_map = {}
            for assign in assignments:
                if assign.staff:
                    name_parts = filter(
                        None, [assign.staff.firstname, assign.staff.lastname]
                    )
                    display_name = assign.staff.display_name or " ".join(name_parts)
                    assignment_map[assign.asset_id] = display_name

            # Map user_name to assets
            result = []
            for asset in assets:
                asset.user_name = assignment_map.get(asset.id)
                result.append(asset)

            return result
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def findById(asset_id, db):
        try:

            asset = (
                db.query(Asset)
                .filter(Asset.id == asset_id)
                .options(
                    joinedload(Asset.device_type),
                    joinedload(Asset.device_model),
                    joinedload(Asset.location),
                    joinedload(Asset.department),
                    joinedload(Asset.cpu),
                    joinedload(Asset.ram),
                    joinedload(Asset.hhd),
                    joinedload(Asset.os),
                    joinedload(Asset.office),
                )
                .first()
            )

            if not asset:
                raise HTTPException(status_code=404, detail="Asset not found")

            # Get active assignment for this asset
            assign = (
                db.query(AssetAssignment)
                .filter(
                    AssetAssignment.asset_id == asset_id,
                    AssetAssignment.is_returned == False,
                )
                .options(joinedload(AssetAssignment.staff))
                .first()
            )

            if assign and assign.staff:
                name_parts = filter(
                    None, [assign.staff.firstname, assign.staff.lastname]
                )
                display_name = assign.staff.display_name or " ".join(name_parts)
                asset.user_name = display_name
            else:
                asset.user_name = None

            return asset
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def created(asset_data, db):
        try:
            data = asset_data.model_dump(exclude_unset=True)
            new_asset = Asset(**data)
            db.add(new_asset)
            db.commit()
            db.refresh(new_asset)
            return new_asset
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def update(asset_id, asset_data, db):
        try:
            asset = db.query(Asset).filter(Asset.id == asset_id).first()
            if not asset:
                raise HTTPException(status_code=404, detail="Asset not found")

            update_data = asset_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(asset, key, value)

            db.commit()
            db.refresh(asset)
            return asset
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def deleted(asset_id, db):
        try:
            asset = db.query(Asset).filter(Asset.id == asset_id).first()
            if not asset:
                raise HTTPException(status_code=404, detail="Asset not found")

            db.delete(asset)
            db.commit()
            return {"message": "Asset deleted successfully"}
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
