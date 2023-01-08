from cassandra.cluster import Cluster, Session
from pymongo import MongoClient
from pymongo.database import Database


def get_cassandra_session() -> Session:
    cluster = Cluster(protocol_version=5)
    session = cluster.connect('market_app', wait_for_all_pools=True)
    session.execute('USE market_app')

    return session

def get_mongo_db_db() -> Database:
    CONNECTION_STRING = "mongodb://root:example@localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['market_app_db']


