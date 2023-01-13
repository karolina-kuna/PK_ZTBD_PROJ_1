from typing import List

from implementation.market_app.models.db_models.postgres_models import Apartment
from implementation.market_app.repositories.repository_dependencies import get_postgres_db


class PostgresApartmentRepository:

    def __init__(self):
        self.conn = get_postgres_db()

    def create_table(self):
        cursor = self.conn.cursor()
        query = f"""
        CREATE TABLE IF NOT EXISTS apartment (
            id SERIAL PRIMARY KEY,
            area DECIMAL(3,2) NOT NULL,
            creation_year INTEGER(4) NOT NULL,
            last_renovation_year INTEGER,
            building_type VARCHAR(14) NOT NULL,
            heating_type VARCHAR(10) NOT NULL,
            is_furnished BOOLEAN NOT NULL,
            rooms_count INTEGER(4) NOT NULL,
            address_id INTEGER REFERENCES address(id) ON DELETE CASCADE,
            owner_id INTEGER NOT NULL REFERENCES owner(id)
        );"""

        cursor.execute(query)
        self.conn.commit()

    def insert(self, apartment: Apartment) -> Apartment:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO apartment (area, creation_year, last_renovation_year, building_type, heating_type,"
                " is_furnished, rooms_count, address_id, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                " RETURNING *",
                (apartment.area, apartment.creation_year, apartment.last_renovation_year, apartment.building_type,
                 apartment.heating_type, apartment.is_furnished, apartment.rooms_count, apartment.address_id,
                 apartment.owner_id))
            inserted_apartment = cur.fetchone()
        self.conn.commit()
        return Apartment(**inserted_apartment)

    def update(self, updated_apartment: Apartment):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE apartment
                SET area = %s, creation_year = %s, last_renovation_year = %s, building_type = %s, heating_type = %s,
                is_furnished = %s, rooms_count = %s, address_id = %s, owner_id = %s
                WHERE id = %s
                """, (updated_apartment.area, updated_apartment.creation_year, updated_apartment.last_renovation_year,
                      updated_apartment.building_type, updated_apartment.heating_type, updated_apartment.is_furnished,
                      updated_apartment.rooms_count), updated_apartment.address_id, updated_apartment.owner_id)
            self.conn.commit()

    def delete(self, apartment_id: int) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM apartment WHERE id = %s", (apartment_id,))
        self.conn.commit()

    def get_by_id(self, apartment_id: int) -> Apartment:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM apartment WHERE id = %s", (apartment_id,))
            result = cursor.fetchone()
        if result:
            return Apartment(*result)
        else:
            return None

    def get_all(self) -> List[Apartment]:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM apartment")
            results = cursor.fetchall()
        return [Apartment(**result) for result in results]
