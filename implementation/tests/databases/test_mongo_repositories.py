from pymongo import MongoClient
from pymongo.database import Database

from market_app.models.db_models.mongodb_models import Owner
from market_app.repositories.mongo_db_owner_repository import MongoDbOwnerRepository


def get_database() -> Database:
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://root:example@localhost:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['market_app_db']


client = get_database()
owner = Owner(surname="Smith", phone_number="123-456-7890",
              address="123 Main St.", email_address="smith@example.com", company_name="Acme Inc.")


mongo_client = MongoClient("mongodb://root:example@localhost:27017")
repository = MongoDbOwnerRepository(client)

# Insert the owner into the database
owner_id = repository.create(owner)

# Update the owner's company name
owner.company_name = "Acme Corp."
repository.update(owner)

# Find the owner by ID
found_owner = repository.get_by_id(owner_id)
print(found_owner)

# Find all owners
all_owners = repository.get_all()

for owner in all_owners:
    print(owner.surname, owner.id)

# # Find owners by company name
owners_by_company_name = repository.find_by_company_name(owner.company_name)
print(len(owners_by_company_name))

repository.delete(owner_id)