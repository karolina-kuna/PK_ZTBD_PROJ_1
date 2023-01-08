from random import random

from market_app.services.mongo_db_service import MongoDbService
from tests.databases.dummy_generator import generate_random_full_apartment

if __name__ == "__main__":
    mongo_db_service = MongoDbService()

    for idx in range(31):
        full_apartment = generate_random_full_apartment(random.randint(1, 6))
        result = mongo_db_service.create_apartment_with_dependencies(full_apartment)
    print("Zapisano w MongoDB:O")
