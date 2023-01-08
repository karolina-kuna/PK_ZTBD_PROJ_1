import string
import random
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database

from market_app.models.db_models.fast_api_mongodb_models import OfferModel, OfferOwnerModel
from market_app.repositories.mongo_db.mongo_db_offer_repository import MongoDbOfferRepository


def generate_offers(n: int):
    offers = []
    for i in range(n):
        id = ObjectId()
        address = {
            "_id": str(ObjectId()),
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston"]),
            "street": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        }
        price = random.uniform(100000.0, 500000.0)
        title = ''.join(random.choices(string.ascii_letters, k=10))
        area = random.uniform(50.0, 200.0)
        owner = OfferOwnerModel(id=str(ObjectId()),
                                company_name=''.join(random.choices(string.ascii_letters, k=10)))

        apartment_id = random.randint(100, 999)
        company_name = ''.join(random.choices(string.ascii_letters, k=10))
        offer = OfferModel(
            id=id,
            address=address,
            price=price,
            title=title,
            area=area,
            owner=owner,
            apartment_id=apartment_id
        )
        offers.append(offer)
    return offers


def get_database() -> Database:
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://root:example@localhost:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['market_app_db']


if __name__ == "__main__":
    client = get_database()
    repository = MongoDbOfferRepository(client)
    offers = generate_offers(1)

    # Insert the owner into the database
    repository.create(offers[0])
