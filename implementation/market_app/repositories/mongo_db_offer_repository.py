from typing import List

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from market_app.models.db_models.mongodb_models import Offer


class MongoDbOfferRepository:
    def __init__(self, database: Database):
        self.collection = database['offer_list']

    def create(self, offer: Offer) -> ObjectId:
        return self.collection.insert_one(offer.__dict__).inserted_id

    def update(self, offer: Offer) -> dict:
        return self.collection.find_one_and_update(
            {"_id": offer.id},
            {"$set": offer.__dict__},
            return_document=ReturnDocument.AFTER
        )

    def delete(self, offer_id: str):
        self.collection.delete_one({"_id": offer_id})

    def get_by_id(self, offer_id: str) -> Offer:
        offer_dict = self.collection.find_one({"_id": offer_id})
        return Offer(**offer_dict) if offer_dict is not None else None

    def get_all(self) -> list:
        return [Offer(**offer_dict) for offer_dict in self.collection.find()]

    def find_by_company_name(self, company_name: str) -> list:
        rows = self.collection.find({"company_name": company_name})
        return [Offer(**offer_dict) for offer_dict in rows]

    def get_offers_by_city_and_address(self, city: str, address: str) -> List[Offer]:
        rows = self.collection.find({"address_city": city, "address_street": address})
        return [Offer(**offer_dict) for offer_dict in rows]

    def get_offers_by_city_and_address_and_price_range(self, city: str, address: str, min_price: int,
                                                       max_price: int) -> list:
        rows = self.collection.find({
            "address_city": city,
            "address_street": address,
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        })
        return [Offer(**offer_dict) for offer_dict in rows]
