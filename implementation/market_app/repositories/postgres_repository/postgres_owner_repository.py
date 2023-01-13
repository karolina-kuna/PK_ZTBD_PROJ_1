from typing import List, Dict

from implementation.market_app.models.db_models.postgres_models import Owner
from implementation.market_app.repositories.repository_dependencies import get_postgres_db


class PostgresOwnerRepository:

    def __init__(self):
        self.conn = get_postgres_db()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS owner (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(255) NOT NULL,
                                surname VARCHAR(255) NOT NULL,
                                phone_number VARCHAR(255) NOT NULL,
                                email_address VARCHAR(255) NOT NULL,
                                company_name VARCHAR(255),
                                address_id INTEGER REFERENCES address(id)
                                );
                        ''')
        self.conn.commit()

    def insert(self, owner: Owner) -> Owner:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO owner (name, surname, phone_number, email_address, company_name, address_id) VALUES (%s, "
                "%s, %s, %s, %s, %s) RETURNING *",
                (owner.name, owner.surname, owner.phone_number, owner.email_address, owner.company_name,
                 owner.address_id),
            )
            inserted_owner = cur.fetchone()
        self.conn.commit()
        return Owner(**inserted_owner)

    def get_by_id(self, id: int) -> Owner:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM owner WHERE id = %s", (id,))
            result = cursor.fetchone()
        if result:
            return Owner(*result)
        else:
            return None

    def update(self, owner: Owner, owner_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE owner SET name = %s, surname = %s, phone_number = %s, email_address = %s, company_name = %s, "
                "address_id = %s WHERE id = %s",
                (owner.name, owner.surname, owner.phone_number, owner.email_address, owner.company_name,
                 owner.address_id, owner_id)
            )
        self.conn.commit()

    def delete(self, owner_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM owner WHERE id = %s", (owner_id,))
        self.conn.commit()

    def get_all(self) -> List[dict]:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM owner")
            owners = cursor.fetchall()
        return [dict(owner) for owner in owners]
