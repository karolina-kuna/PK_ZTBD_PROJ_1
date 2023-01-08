import random
from market_app.services.cassandra_service import CassandraService
from tests.databases.dummy_generator import generate_random_full_apartment

if __name__ == "__main__":
    cassandra_service = CassandraService()

    for idx in range(31):
        full_apartment = generate_random_full_apartment(random.randint(1, 6))
        result = cassandra_service.create_apartment_with_dependencies(full_apartment)
    print("Zapisano :O")
