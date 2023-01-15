from datetime import date
from typing import List

from implementation.market_app.models.api_models import ApartmentOfferAveragePrice, CompanyStatisticResult, \
    SaleOfferStatusUpdate
from implementation.market_app.models.postgres_models import Offer
from implementation.market_app.repositories.repository_dependencies import get_postgres_db


class PostgresOfferRepository:

    def __init__(self):
        self.connection = get_postgres_db()

    def create_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
                CREATE TABLE IF NOT EXISTS offer (
                    id SERIAL PRIMARY KEY,
                    price DECIMAL(8,2) NOT NULL,
                    status VARCHAR(8) NOT NULL,
                    negotiable BOOLEAN NOT NULL,
                    description VARCHAR(300),
                    agency_fee DECIMAL(8,2),
                    creation_date DATE NOT NULL,
                    modification_date DATE,
                    apartment_id INTEGER REFERENCES apartment(id) ON DELETE CASCADE
                );
            """
        cursor.execute(create_table_query)
        self.connection.commit()

    def insert(self, sale_offer: Offer) -> Offer:
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO offer (price, status, negotiable, description, agency_fee, creation_date,modification_date,apartment_id) VALUES (%s, %s, %s, "
                "%s, %s,%s,%s,%s) RETURNING id",
                (sale_offer.price, sale_offer.status, sale_offer.negotiable, sale_offer.description,sale_offer.agency_fee, sale_offer.creation_date,sale_offer.modification_date,sale_offer.apartment_id),
            )
            new_id = cur.fetchone()[0]
        self.connection.commit()
        return new_id

    def get_offers_by_city_and_address(self, city: str, street: str) -> List[Offer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * from offer where apartment_id in (SELECT apartment_id from apartment where address_id in 
                (SELECT address_id from address where city = %s and street_name = %s));
                """, (city, street))
            offers = cursor.fetchall()
        return [
            Offer(offer[0], offer[1], offer[2], offer[3], offer[4],
                  offer[5], offer[6], offer[7], offer[8]) for offer
            in offers]

    def get_offers_by_city_and_price_range(self, city: str, min_price: float, max_price: float) -> List[Offer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM offer as so 
                JOIN apartment as ap on so.apartment_id = ap.id 
                JOIN address as ad on ap.address_id = ad.id 
                WHERE ad.city = %s and so.price BETWEEN %s and %s
                """, (city, min_price, max_price))
            offers = cursor.fetchall()
        return [
            Offer(offer[0], offer[1], offer[2], offer[3], offer[4],
                  offer[5], offer[6], offer[7], offer[9]) for offer
            in offers]

    def get_offers_by_company_name(self, company_name: str) -> List[Offer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM offer as so 
                JOIN apartment as ap on so.apartment_id = ap.id 
                JOIN owner as ow on ap.owner_id = ow.id 
                WHERE ow.company_name = %s
                """, (company_name,))
            offers = cursor.fetchall()
        return [
            Offer(offer[0], offer[1], offer[2], offer[3], offer[4],
                  offer[5], offer[6], offer[7], offer[8]) for offer
            in offers]

    ## chyba nie ma sensu?
    # def get_offers_by_city_and_price_and_id(self, city: str, price: float, id: int) -> List[
    #     SaleOffer]:
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(
    #             """
    #             SELECT * FROM sale_offer as so
    #             JOIN apartment as ap on so.apartment_id = ap.id
    #             JOIN address as ad on ap.address_id = ad.id
    #             WHERE ad.city = %s and so.price = %s and so.id = %s
    #             """, (city, price, id))
    #         offers = cursor.fetchall()
    #         offers_list = []
    #     for offer in offers:
    #         sale_offer = SaleOffer(offer_id=offer['offer_id'],
    #                                price=offer['price'],
    #                                status=offer['status'],
    #                                negotiable=offer['negotiable'],
    #                                description=offer['description'],
    #                                agency_fee=offer['agency_fee'],
    #                                creation_date=offer['creation_date'],
    #                                modification_date=offer['modification_date'],
    #                                apartment_id=offer['apartment_id']
    #                                )
    #         offers_list.append(sale_offer)
    #         return offers_list

    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> Offer:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE offer
                SET status = %s
                WHERE id = %s
                RETURNING *
            """, (update_info.status, offer_id))
            self.connection.commit()
            updated_offer = cursor.fetchone()
        return Offer(*updated_offer)

    def get_average_price_by_city(self, city: str) -> List[ApartmentOfferAveragePrice]:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT ad.city, AVG(so.price) as avg_price, AVG(so.price/ap.area) as avg_price_per_m2
                FROM offer as so
                JOIN apartment as ap on so.apartment_id = ap.id
                JOIN address as ad on ap.address_id = ad.id
                WHERE ad.city = %s
                GROUP BY ad.city
            """, (city,))
            result = cursor.fetchall()
        return [ApartmentOfferAveragePrice(city=row[0], avg_price=row[1], avg_price_per_m2=row[2]) for row in result]

    def get_companies_sales_statistics(self, company_name: str) -> List[CompanyStatisticResult]:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    ow.company_name as company_name,
                    COUNT(so.id) as total_sales,
                    SUM(so.price) as total_sales_price,
                    AVG(so.price) as average_sales_price
                FROM offer as so
                JOIN apartment as ap on so.apartment_id = ap.id
                JOIN owner as ow on ap.owner_id = ow.id
                WHERE ow.company_name = %s
                GROUP BY ow.company_name
            """, (company_name,))
            result = cursor.fetchall()
        return [CompanyStatisticResult(company_name=row[0], total_sales=row[1], total_sales_price=row[2],
                                       average_sales_price=row[3]) for row in result]

    def get_statistic_by_company(self, company_filter: str) -> List[CompanyStatisticResult]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT company_name, 
                       AVG(price) as avg_price, 
                       AVG(price/area) as avg_price_per_m2, 
                       COUNT(*) as sales_offer_count 
                FROM market_app.offers_by_company_name 
                WHERE company_name = %s
                GROUP BY company_name
                """, (company_filter,))
            results = cursor.fetchall()
        return [CompanyStatisticResult(company_name=row[0],
                                       avg_price=row[1],
                                       avg_price_per_m2=row[2],
                                       sales_offer_count=row[3])
                for row in results]

    def delete(self, id: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM offer WHERE id = %s", (id,))
            self.connection.commit()

    def update(self, id: int, price: float, status: str, negotiable: bool, description: str, agency_fee: float,
               creation_date: date, modification_date: date, apartment_id: int) -> Offer:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE offer
                SET price = %s, status = %s, negotiable = %s, description = %s, agency_fee = %s,
                creation_date = %s, modification_date = %s,
                apartment_id = %s
                WHERE id = %s
                """, (
                price, status, negotiable, description, agency_fee, creation_date, modification_date, apartment_id, id))
            self.connection.commit()

        updated_offer = self.get_by_id(id)
        return updated_offer

    def get_by_id(self, sale_offer_id: int) -> Offer | None:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM offer WHERE id = %s", (sale_offer_id,))
            result = cursor.fetchone()
        if result:
            return Offer(*result)
        else:
            return None

    def get_all(self) -> List[Offer]:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM offer")
            results = cursor.fetchall()
        return [Offer(*result) for result in results]
