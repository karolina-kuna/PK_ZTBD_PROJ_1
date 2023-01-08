from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import AddressModel


class MongoDbAddressRepository:

    def __init__(self, database: Database):
        self.collection = database['address_list']

    def create(self, address: AddressModel) -> ObjectId:
        return self.collection.insert_one(address.__dict__).inserted_id

    def update(self, address: AddressModel) -> dict:
        return self.collection.find_one_and_update(
            {"_id": address.id},
            {"$set": address.__dict__},
            return_document=ReturnDocument.AFTER
        )

    def delete(self, address_id: str):
        self.collection.delete_one({"_id": address_id})

    def get_by_id(self, address_id: str) -> AddressModel:
        address_dict = self.collection.find_one({"_id": address_id})
        return AddressModel(**address_dict) if address_dict is not None else None

    def get_all(self) -> list:
        return [AddressModel(**address_dict) for address_dict in self.collection.find()]