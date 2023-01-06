from typing import List

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from market_app.models.db_models.cassandra_models import Apartment
from market_app.repositories.uuid_util import convert_uuid_into_text, convert_text_into_uuid, generate_uuid


class CassandraApartmentRepository:
    def __init__(self, cluster: Cluster):
        self.key_space = "market_app"
        self.session = cluster.connect(self.key_space)

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS apartment (apartment_id uuid PRIMARY KEY, area int, creation_year int, last_renovation_year int, building_type text, heating_type text, is_furnished boolean, rooms_count int, owner_id: text, address_id: text)"
        self.session.execute(query)

    def insert(self, apartment: Apartment) -> Apartment:
        query = SimpleStatement(
            "INSERT INTO apartment (apartment_id, area, creation_year, last_renovation_year, building_type, heating_type, is_furnished, rooms_count, owner_id, address_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            consistency_level=ConsistencyLevel.QUORUM
        )
        apartment_id_uuid = generate_uuid()
        self.session.execute(query, (
            apartment_id_uuid, apartment.area, apartment.creation_year, apartment.last_renovation_year,
            apartment.building_type, apartment.heating_type, apartment.is_furnished, apartment.rooms_count,
            apartment.owner_id, apartment.address_id
        ))
        apartment.apartment_id = convert_uuid_into_text(apartment_id_uuid)
        return apartment

    def update(self, apartment: Apartment) -> Apartment:
        query = SimpleStatement(
            "UPDATE apartment SET area=%s, creation_year=%s, last_renovation_year=%s, building_type=%s, heating_type=%s, is_furnished=%s, rooms_count=%s, owner_id=%s, address_id=%s WHERE apartment_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        apartment_id_uuid = convert_text_into_uuid(apartment.apartment_id)
        self.session.execute(query, (
            apartment.area, apartment.creation_year, apartment.last_renovation_year, apartment.building_type,
            apartment.heating_type, apartment.is_furnished, apartment.rooms_count, apartment.owner_id,
            apartment.address_id, apartment_id_uuid))
        return apartment

    def delete(self, apartment_id: str):
        query = SimpleStatement(
            "DELETE FROM apartment WHERE apartment_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        apartment_id_uuid = convert_text_into_uuid(apartment_id)
        self.session.execute(query, apartment_id_uuid)

    def get_by_id(self, apartment_id: str) -> Apartment:
        query = SimpleStatement(
            "SELECT * FROM apartment WHERE apartment_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        row = self.session.execute(query, convert_text_into_uuid(apartment_id)).one()
        return self.__map_row_to_apartment(row)

    def get_all(self) -> List[Apartment]:
        query = SimpleStatement(
            "SELECT * FROM apartment",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query)
        return [self.__map_row_to_apartment(row) for row in rows]

    def __map_row_to_apartment(self, row) -> Apartment:
        return Apartment(convert_uuid_into_text(row.apartment_id), row.area, row.creation_year,
                         row.last_renovation_year, row.building_type,
                         row.heating_type, row.is_furnished, row.rooms_count, row.owner_id, row.address_id)
