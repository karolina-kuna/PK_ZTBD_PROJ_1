from typing import List

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import OfferModel


class MongoDbOfferRepository:
    def __init__(self, database: Database):
        self.collection = database['offer_list']

    def create(self, offer: OfferModel) -> ObjectId:
        return self.collection.insert_one(offer.__dict__).inserted_id

    def update(self, offer: OfferModel) -> dict:
        return self.collection.find_one_and_update(
            {"_id": offer.id},
            {"$set": offer.__dict__},
            return_document=ReturnDocument.AFTER
        )

    def delete(self, offer_id: str):
        self.collection.delete_one({"_id": offer_id})

    def get_by_id(self, offer_id: str) -> OfferModel:
        offer_dict = self.collection.find_one({"_id": offer_id})
        return OfferModel(**offer_dict) if offer_dict is not None else None

    def get_all(self) -> list:
        return [OfferModel(**offer_dict) for offer_dict in self.collection.find()]

    def find_by_company_name(self, company_name: str) -> list:
        rows = self.collection.find({"owner.company": company_name})
        return [OfferModel(**offer_dict) for offer_dict in rows]

    def get_offers_by_city_and_address(self, city: str, address: str) -> List[OfferModel]:
        rows = self.collection.find({"address.city": city, "address.street": address})
        return [OfferModel(**offer_dict) for offer_dict in rows]

    def get_offers_by_city_and_price_range(self, city: str,
                                           min_price: float,
                                           max_price: float) -> list:
        rows = self.collection.find({
            "address.city": city,
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        })
        return [OfferModel(**offer_dict) for offer_dict in rows]
