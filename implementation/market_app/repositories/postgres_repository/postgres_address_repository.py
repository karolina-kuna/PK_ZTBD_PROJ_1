from typing import List

from psycopg2.extras import RealDictCursor

from implementation.market_app.models.db_models.postgres_models import Address
from implementation.market_app.repositories.repository_dependencies import get_postgres_db


class PostgresAddressRepository:

    def __init__(self):
        self.conn = get_postgres_db()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS address (
                                       id SERIAL PRIMARY KEY,
                                       city VARCHAR(255) NOT NULL,
                                       street_name VARCHAR(255) NOT NULL,
                                       building_nr VARCHAR(255) NOT NULL,
                                       apartment_nr VARCHAR(255) NOT NULL,
                                       postal_code VARCHAR(255) NOT NULL);
                               ''')
        self.conn.commit()

    def insert(self, address: Address) -> Address:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO address (city, street_name, building_nr, apartment_nr, postal_code) VALUES (%s, %s, %s, "
                "%s, %s) RETURNING id",
                (address.city, address.street_name, address.building_nr, address.apartment_nr, address.postal_code),
            )
            new_id = cur.fetchone()[0]
        self.conn.commit()
        return new_id

    def update(self, address: Address, address_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE address SET city = %s, street_name = %s, building_nr = %s, apartment_nr = %s,postal_code = %s "
                "WHERE id = %s",
                (address.city, address.street_name, address.building_nr, address.apartment_nr, address.postal_code,
                 address_id),
            )
        self.conn.commit()

    def delete(self, address_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM address WHERE id = %s", (address_id,))
        self.conn.commit()

    def find_by_id(self, address_id: int) -> Address:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM address WHERE id = %s", (address_id,))
            address_data = cur.fetchone()
        if address_data:
            return Address(address_data['id'], address_data["city"], address_data["street_name"],
                           address_data["building_nr"],
                           address_data["apartment_nr"], address_data["postal_code"])
        else:
            return None

    def find_by_city_and_street(self, city: str, street: str) -> List[Address]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM address WHERE city = %s AND street = %s", (city, street))
            addresses_data = cur.fetchall()
        if addresses_data:
            return [
                Address(addresses_data['id'], address_data["city"], address_data["street_name"],
                        address_data["building_nr"],
                        address_data["apartment_nr"], address_data["postal_code"])
                for address_data in addresses_data
            ]
        else:
            raise ValueError("Addresses not found in database")
