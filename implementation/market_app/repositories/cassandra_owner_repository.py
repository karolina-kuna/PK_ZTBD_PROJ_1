import uuid
from typing import List

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from market_app.models.db_models.cassandra_models import Owner
from market_app.repositories.uuid_util import generate_uuid, convert_text_into_uuid, convert_uuid_into_text


class CassandraOwnerRepository:
    def __init__(self, cluster: Cluster):
        self.session = cluster.connect()
        self.key_space = "market_app"

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS {self.key_space}.owner (owner_id uuid PRIMARY KEY, surname text, phone_number text, address text, email_address text, company_name text)"
        self.session.execute(query)

    def insert(self, owner: Owner) -> Owner:
        query = SimpleStatement(
            f"INSERT INTO {self.key_space}.owner (owner_id, surname, phone_number, address, email_address, company_name) VALUES (%s, %s, %s, %s, %s, %s)",
            consistency_level=ConsistencyLevel.QUORUM
        )
        owner_id = generate_uuid()
        self.session.execute(query, (
            owner_id, owner.surname, owner.phone_number, owner.address, owner.email_address, owner.company_name))
        owner.owner_id = convert_uuid_into_text(owner_id)
        return owner

    def update(self, owner: Owner) -> Owner:
        query = SimpleStatement(
            f"UPDATE {self.key_space}.owner SET surname=%s, phone_number=%s, address=%s, email_address=%s, company_name=%s WHERE owner_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        owner_id_uuid = convert_text_into_uuid(owner.owner_id)
        self.session.execute(query, (
            owner.surname, owner.phone_number, owner.address, owner.email_address, owner.company_name, owner_id_uuid))
        return owner

    def delete(self, owner_id: uuid) -> bool:
        query = SimpleStatement(
            f"DELETE FROM {self.key_space}.owner WHERE owner_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        owner_id_uuid = convert_text_into_uuid(owner_id)
        self.session.execute(query, owner_id_uuid)
        return True

    def get_by_id(self, owner_id: uuid) -> Owner:
        query = SimpleStatement(
            f"SELECT * FROM {self.key_space}.owner WHERE owner_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        owner_id_uuid = convert_text_into_uuid(owner_id)
        row = self.session.execute(query, owner_id_uuid).one()
        return self.__map_row_to_owner(row)

    def get_all(self) -> List[Owner]:
        query = SimpleStatement(
            f"SELECT * FROM {self.key_space}.owner",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query)
        return [self.__map_row_to_owner(row) for row in rows]

    def __map_row_to_owner(self, row) -> Owner:
        return Owner(convert_uuid_into_text(row.owner_id), row.surname, row.name, row.phone_number, row.address,
                     row.email_address, row.company_name)
