from pymongo import ReturnDocument
from bson.objectid import ObjectId
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import OwnerModel


class MongoDbOwnerRepository:
    def __init__(self, database: Database):
        self.collection = database['owner_list']

    def create(self, owner: OwnerModel) -> ObjectId:
        return self.collection.insert_one(owner.__dict__).inserted_id

    def update(self, owner: OwnerModel) -> dict:
        return self.collection.find_one_and_update(
            {"_id": owner.id},
            {"$set": owner.__dict__},
            return_document=ReturnDocument.AFTER
        )

    def delete(self, owner_id: str):
        self.collection.delete_one({"_id": owner_id})

    def get_by_id(self, owner_id: str) -> OwnerModel:
        owner_dict = self.collection.find_one({"_id": ObjectId(owner_id)})
        return OwnerModel(**owner_dict) if owner_dict is not None else None

    def get_all(self) -> list:
        return [OwnerModel(**owner_dict) for owner_dict in self.collection.find()]

    def find_by_company_name(self, company_name: str) -> list:
        rows = self.collection.find({"company_name": company_name})
        return [OwnerModel(**owner_dict) for owner_dict in rows]
