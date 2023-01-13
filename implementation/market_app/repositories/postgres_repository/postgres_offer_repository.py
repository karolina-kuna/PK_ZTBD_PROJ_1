from datetime import date
from typing import List, Dict

from implementation.market_app.models.api_models import ApartmentOfferAveragePrice, CompanyStatisticResult, \
    SaleOfferStatusUpdate
from implementation.market_app.models.db_models.postgres_models import SaleOffer
from implementation.market_app.repositories.repository_dependencies import get_postgres_db


class PostgresOfferRepository:

    def __init__(self):
        self.connection = get_postgres_db()

    def create_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
                CREATE TABLE IF NOT EXISTS sale_offer (
                    id SERIAL PRIMARY KEY,
                    creation_date DATE NOT NULL,
                    price DECIMAL(8,2) NOT NULL,
                    negotiable BOOLEAN NOT NULL,
                    status VARCHAR(8) NOT NULL,
                    modification_date DATE,
                    description VARCHAR(300),
                    agency_fee DECIMAL(8,2),
                    apartment_id INTEGER REFERENCES apartment(id) ON DELETE CASCADE
                );
            """
        cursor.execute(create_table_query)
        self.connection.commit()

    def insert(self, sale_offer: SaleOffer) -> SaleOffer:
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO Sale_Offer (creation_date, price, negotiable, status,modification_date,"
                "description,agency_fee,apartment_id) VALUES (%s, %s, %s, "
                "%s, %s,%s,%s,%s",
                (sale_offer.creation_date, sale_offer.price, sale_offer.negotiable, sale_offer.status,
                 sale_offer.modification_date, sale_offer.description, sale_offer.agency_fee, sale_offer.apartment_id),
            )
            new_id = cur.fetchone()[0]
        self.connection.commit()
        return new_id

    def get_offers_by_city_and_address(self, city: str, street: str) -> List[SaleOffer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * from sale_offer where apartment_id in (SELECT apartment_id from apartment where address_id in 
                (SELECT address_id from address where city = '%s' and street_name = '%s'));
                """, (city, street))
            offers = cursor.fetchall()
        return [
            SaleOffer(offer['id'], offer['apartment_id'], offer['price'], offer['created_date'], offer['description'],
                      offer['negotiable'], offer['agency_fee'], offer['modification_date'], offer['status']) for offer
            in offers]

    def get_offers_by_city_and_price_range(self, city: str, min_price: float, max_price: float) -> List[SaleOffer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM sale_offer as so 
                JOIN apartment as ap on so.apartment_id = ap.id 
                JOIN address as ad on ap.address_id = ad.id 
                WHERE ad.city = %s and so.price BETWEEN %s and %s
                """, (city, min_price, max_price))
            offers = cursor.fetchall()
        return [
            SaleOffer(offer['id'], offer['apartment_id'], offer['price'], offer['created_date'], offer['description'],
                      offer['negotiable'], offer['agency_fee'], offer['modification_date'], offer['status']) for offer
            in offers]

    def get_offers_by_company_name(self, company_name: str) -> List[SaleOffer]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM sale_offer as so 
                JOIN apartment as ap on so.apartment_id = ap.id 
                JOIN owner as ow on ap.owner_id = ow.id 
                WHERE ow.company_name = %s
                """, (company_name,))
            offers = cursor.fetchall()
        return [
            SaleOffer(offer['id'], offer['apartment_id'], offer['price'], offer['created_date'], offer['description'],
                      offer['negotiable'], offer['agency_fee'], offer['modification_date'], offer['status']) for offer
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

    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sale_offer
                SET status = %s
                WHERE id = %s
                RETURNING *
            """, (update_info.status, offer_id))
            updated_offer = cursor.fetchone()
        return SaleOffer(**updated_offer)

    def get_average_price_by_city(self, city: str) -> List[ApartmentOfferAveragePrice]:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT ad.city, AVG(so.price) as avg_price, AVG(so.price/ap.area) as avg_price_per_m2
                FROM sale_offer as so
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
                FROM sale_offer as so
                JOIN apartment as ap on so.apartment_id = ap.id
                JOIN owner as ow on ap.owner_id = ow.id
                WHERE ow.company_name = %s
                GROUP BY ow.company_name
            """, (company_name,))
            result = cursor.fetchall()
        return [CompanyStatisticResult(company_name=row[0], total_sales=row[1], total_sales_price=row[2],
                                       average_sales_price=row[3]) for row in result]

    def get_statistic_by_company(self, company_name: str) -> CompanyStatisticResult:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(so.id) as number_of_offers, SUM(so.price) as total_price, AVG(so.price) as average_price
                FROM sale_offer as so
                JOIN apartment as ap on so.apartment_id = ap.id
                JOIN owner as ow on ap.owner_id = ow.id
                WHERE ow.company_name = %s
                """, (company_name,))
            result = cursor.fetchone()
        if result:
            return CompanyStatisticResult(company_name=result.company_name,
                                          avg_price=result.avg_price,
                                          avg_price_per_m2=result.avg_price_per_m2,
                                          sales_offer_count=result.sales_offer_count
                                          )
        else:
            return None

    def delete(self, id: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM sale_offer WHERE id = %s", (id,))
            self.connection.commit()

    def update(self, creation_date: date, price: float, negotiable: bool, status: str, modification_date: date,
               description: str, agency_fee: float, apartment_id: int, id: int) -> SaleOffer:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sale_offer
                SET creation_date = %s, price = %s, negotiable = %s, status = %s, modification_date = %s,
                description = %s, agency_fee = %s,
                apartment_id = %s
                WHERE id = %s
                """, (
                creation_date, price, negotiable, status, modification_date, description, agency_fee, apartment_id, id))
            self.connection.commit()

        updated_offer = self.get_by_id(id)
        return updated_offer

    def get_by_id(self, sale_offer_id: int) -> SaleOffer:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sale_offer WHERE id = %s", (sale_offer_id,))
            result = cursor.fetchone()
        if result:
            return SaleOffer(*result)
        else:
            return None

    def get_all(self) -> List[SaleOffer]:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sale_offer")
            results = cursor.fetchall()
        return [SaleOffer(**result) for result in results]
