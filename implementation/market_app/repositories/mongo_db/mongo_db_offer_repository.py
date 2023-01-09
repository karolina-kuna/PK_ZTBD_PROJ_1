from typing import List

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import OfferModel

from market_app.models.api_models import ApartmentOfferAveragePrice, CompanyStatisticResult


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

    def get_by_id(self, offer_id: str) -> OfferModel | None:
        try:
            offer_id_object_id = ObjectId(offer_id)
        except Exception:
            return None

        offer_dict = self.collection.find_one({"_id": ObjectId(offer_id)})
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

    def get_companies_sales_statistics(self, company_name: str) -> List[CompanyStatisticResult]:
        pipeline = []
        if company_name:
            company_name_match = {
                '$match': {
                    'owner.company_name': f"{company_name}"
                }
            }
            pipeline.append(company_name_match)

        pipeline.append({
            '$group': {
                '_id': '$owner.company_name',
                'avg_price_per_m2': {'$avg': {'$divide': ['$price', '$area']}},
                'avg_price': {'$avg': '$price'},
                'sales_offer_count': {'$count': {}}
            }
        })

        result = self.collection.aggregate(pipeline)

        company_statistics = []
        for doc in result:
            average_price = CompanyStatisticResult(
                company_name=doc['_id'],
                avg_price_per_m2=doc['avg_price_per_m2'],
                avg_price=doc['avg_price'],
                sales_offer_count=doc['sales_offer_count']
            )
            company_statistics.append(average_price)

        return company_statistics

    def get_average_price_by_city(self, city_name: str) -> List[ApartmentOfferAveragePrice]:
        pipeline = []

        if city_name:
            city_match = {
                '$match': {
                    'address.city': f"{city_name}"
                }
            }
            pipeline.append(city_match)

        pipeline.append({
            '$group': {
                '_id': '$address.city',
                'avg_price_per_m2': {'$avg': {'$divide': ['$price', '$area']}},
                'avg_price': {'$avg': '$price'}
            }
        })

        result = self.collection.aggregate(pipeline)

        apartmentsOfferAveragePrice = []
        for doc in result:
            average_price = ApartmentOfferAveragePrice(
                city=doc['_id'],
                avg_price_per_m2=doc['avg_price_per_m2'],
                avg_price=doc['avg_price']
            )
            apartmentsOfferAveragePrice.append(average_price)

        return apartmentsOfferAveragePrice
