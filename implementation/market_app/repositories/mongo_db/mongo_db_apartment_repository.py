from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import ApartmentModel


class MongoDbApartmentRepository:

    def __init__(self, database: Database):
        self.collection = database['apartment_list']

    def create(self, apartment: ApartmentModel) -> ObjectId:
        return self.collection.insert_one(apartment.__dict__).inserted_id

    def update(self, apartment: ApartmentModel) -> dict:
        return self.collection.find_one_and_update(
            {"_id": apartment.id},
            {"$set": apartment.__dict__},
            return_document=ReturnDocument.AFTER
        )

    def delete(self, apartment_id: str):
        self.collection.delete_one({"_id": apartment_id})

    def get_by_id(self, apartment_id: str) -> ApartmentModel:
        apartment_dict = self.collection.find_one({"_id": ObjectId(apartment_id)})
        return ApartmentModel(**apartment_dict) if apartment_dict is not None else None

    def get_all(self) -> list:
        return [ApartmentModel(**apartment_dict) for apartment_dict in self.collection.find()]


