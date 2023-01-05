from cassandra.cluster import Cluster
from fastapi import Depends

from market_app.repositories.cassandra_owner_repository import CassandraOwnerRepository


def get_cassandra_cluster() -> Cluster:
    db: Cluster = Cluster()
    try:
        yield db
    finally:
        print("FINAL DB")


def get_cassandra_owner_repository(
        cluster: Cluster = Depends(get_cassandra_cluster)
):
    print("cluster")
    print(cluster)
    repository = CassandraOwnerRepository(cluster)
    yield repository
