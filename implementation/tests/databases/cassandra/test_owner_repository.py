# Connect to Cassandra cluster
import uuid

from cassandra.cluster import Cluster

from market_app.models.db_models.cassandra_models import Owner
from market_app.repositories.cassandra_owner_repository import CassandraOwnerRepository

cluster = Cluster()

# Create an instance of the CassandraOwnerRepository
repository = CassandraOwnerRepository(cluster)
# Create the owner table
# repository.create_table()

# Insert an owner
owner = Owner(uuid.uuid4(), "Smith", "+1234567890", "123 Main St", "smith@example.com", "Real Estate LLC")
repository.insert(owner)

# Update an owner
owner.surname = "Jones"
owner.phone_number = "+0987654321"
repository.update(owner)

# Delete an owner
repository.delete(owner.owner_id)

# Get an owner by ID
owner = repository.get_by_id(uuid.uuid4())

# Get all owners
owners = repository.get_all()

# Disconnect from the cluster
cluster.shutdown()