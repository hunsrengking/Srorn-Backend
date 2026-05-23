from app.features.assets.service import AssetService

class AssetController:

    # assets
    @staticmethod
    def getAssetsTemplate(db):
        return AssetService.getAssetsTemplate(db)

    @staticmethod
    def creates(asset_data, db):
        return AssetService.created(asset_data, db)

    @staticmethod
    def findAll(db):
        return AssetService.findAll(db)

    @staticmethod
    def findById(asset_id, db):
        return AssetService.findById(asset_id, db)

    @staticmethod
    def updated(asset_id, asset_data, db):
        return AssetService.update(asset_id, asset_data, db)

    @staticmethod
    def deleted(asset_id, db):
        return AssetService.deleted(asset_id, db)