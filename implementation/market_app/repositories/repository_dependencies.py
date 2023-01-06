from cassandra.cluster import Cluster, Session
from fastapi import Depends

from market_app.repositories.cassandra_owner_repository import CassandraOwnerRepository


def get_cassandra_session() -> Session:
    cluster = Cluster(protocol_version=5)
    session = cluster.connect('market_app', wait_for_all_pools=True)
    session.execute('USE market_app')

    return session


