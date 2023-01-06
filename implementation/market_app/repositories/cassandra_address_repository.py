import uuid
from typing import List

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, Session
from cassandra.query import SimpleStatement

from market_app.models.db_models.cassandra_models import Address
from market_app.repositories.uuid_util import generate_uuid, convert_text_into_uuid, convert_uuid_into_text


class CassandraAddressRepository:
    def __init__(self, session: Session):
        self.session = session
        self.key_space = "market_app"

    def create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS {self.key_space}.address (address_id uuid PRIMARY KEY, city text, street_name text, building_nr text, apartment_nr text, postal_code text)"
        self.session.execute(query)

    def insert(self, address: Address) -> Address:
        query = SimpleStatement(
            f"INSERT INTO {self.key_space}.address (address_id, city, street_name, building_nr, apartment_nr, postal_code) VALUES (%s, %s, %s, %s, %s, %s)",
            consistency_level=ConsistencyLevel.QUORUM
        )
        address_id = generate_uuid()
        self.session.execute(query,
                             (address_id, address.city, address.street_name, address.building_nr, address.apartment_nr,
                              address.postal_code))
        address.address_id = convert_uuid_into_text(address_id)
        return address

    def update(self, address: Address) -> Address:
        query = SimpleStatement(
            f"UPDATE {self.key_space}.address SET city=%s, street_name=%s, building_nr=%s, apartment_nr=%s, postal_code=%s WHERE address_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        address_id_uuid = convert_text_into_uuid(address.address_id)
        self.session.execute(query, (
            address.city, address.street_name, address.building_nr, address.apartment_nr, address.postal_code,
            address_id_uuid))
        return address

    def delete(self, address_id: uuid) -> bool:
        query = SimpleStatement(
            f"DELETE FROM {self.key_space}.address WHERE address_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        address_id_uuid = convert_text_into_uuid(address_id)
        self.session.execute(query, address_id_uuid)
        return True

    def find_by_id(self, address_id: uuid) -> Address:
        query = SimpleStatement(
            f"SELECT * FROM {self.key_space}.address WHERE address_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        address_id_uuid = convert_text_into_uuid(address_id)
        row = self.session.execute(query, address_id_uuid).one()
        return self.__map_row_to_address(row)

    def find_by_city_and_street(self, city: str, street: str) -> List[Address]:
        query = SimpleStatement(
            f"SELECT * FROM {self.key_space}.address WHERE city=%s AND street=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query, (city, street))
        return [self.__map_row_to_address(row) for row in rows]
