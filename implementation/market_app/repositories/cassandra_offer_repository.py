import time
import copy
from typing import List

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, Session
from cassandra.query import SimpleStatement

from market_app.models.api_models import ApartmentOfferAveragePrice, CompanyStatisticResult
from market_app.models.db_models.cassandra_models import Offer, Apartment, Owner
from market_app.repositories.uuid_util import convert_text_into_uuid, generate_uuid, convert_uuid_into_text


class CassandraOfferRepository:
    def __init__(self, session: Session):
        self.session = session
        self.key_space = "market_app"

    def get_offers_by_city_and_address(self, city: str, address: str) -> List[Offer]:
        query = f"SELECT * FROM {self.key_space}.offers_by_city_and_street WHERE address_city = %s AND address_street = %s"
        rows = self.session.execute(query, (city, address))
        return self.__map_from_rows(rows);

    def get_offers_by_city_and_price_range(self, city: str, min_price: float, max_price: float) -> List[Offer]:
        query = SimpleStatement(
            f"SELECT * FROM {self.key_space}.offers_by_city_and_price WHERE address_city=%s AND price>=%s AND price<=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query, (city, min_price, max_price))
        return self.__map_from_rows(rows)

    def get_offers_by_company_name(self, company_name: str) -> List[Offer]:
        query = SimpleStatement(
            "SELECT * FROM offers_by_company_name WHERE company_name=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query, company_name)
        return self.__map_from_rows(rows)

    def get_offers_by_city_and_price_and_id(self, city: str, price: float, offer_id: str) -> Offer | None:
        offer_uuid = convert_text_into_uuid(offer_id)
        query = SimpleStatement(
            "SELECT * FROM offers_by_city_and_price WHERE address_city=%s AND price=%s AND offer_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        row = self.session.execute(query, (city, price, offer_uuid)).one()
        if not row:
            return None
        return self.__map_from_row(row)

    def get_offer_basic_by_id(self, offer_id: str) -> Offer:
        offer_uuid = convert_text_into_uuid(offer_id)
        query = SimpleStatement(
            "SELECT * FROM offers_basic WHERE offer_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        rows = self.session.execute(query, (offer_uuid,))
        mapped_rows = self.__map_from_rows(rows)
        return mapped_rows[0] if len(mapped_rows) > 0 else None

    def get_average_price_by_city(self, city_filter) -> List[ApartmentOfferAveragePrice]:
        city_filter_query = ""
        if city_filter:
            city_filter_query = f" WHERE address_city ='{city_filter}'";

        query = SimpleStatement(
            f"SELECT address_city, avg(price) as avg_price, avg(price/area) as avg_price_per_m2"
            f" FROM offers_by_city_and_price"
            f"{city_filter_query}"
            f" group by address_city"
        )

        rows = self.session.execute(query)
        return list(map(lambda x: self.__map_average_price(x), rows))

    def get_statistic_by_company(self, company_filter) -> List[CompanyStatisticResult]:
        company_filter_query = ""
        if company_filter:
            company_filter_query = f" WHERE company_name ='{company_filter}'";

        query = SimpleStatement(f"select company_name,"
                                f"avg(price)  as avg_price,"
                                f"avg(price/area) as avg_price_per_m2,"
                                f"count(*) as sales_offer_count "
                                f"{company_filter_query} "
                                f"from market_app.offers_by_company_name group by company_name"
                                )

        rows = self.session.execute(query)
        return list(map(lambda x: self.__map_company_statistic(x), rows))

    def delete(self, offer_id: str):
        offer_basic = self.get_offer_basic_by_id(offer_id)
        if not offer_basic:
            raise ValueError("Not found offer with provided id")

        query = SimpleStatement(
            "DELETE FROM offers_by_company_name WHERE company_name=%s AND offer_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        offer_id_uuid = convert_text_into_uuid(offer_id)
        if offer_basic.company_name:
            self.session.execute(query, (offer_basic.company_name, offer_id_uuid))

        query = SimpleStatement(
            "DELETE FROM offers_by_city_and_street WHERE address_city=%s AND address_street=%s AND offer_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        self.session.execute(query, (offer_basic.address_city, offer_basic.address_street, offer_id_uuid))

        query = SimpleStatement(
            "DELETE FROM offers_by_city_and_price WHERE address_city=%s AND price=%s AND offer_id=%s",
            consistency_level=ConsistencyLevel.QUORUM
        )
        self.session.execute(query, (offer_basic.address_city, offer_basic.price, offer_id_uuid))

    def insert(self, offer: Offer) -> Offer:
        offer_id = generate_uuid()
        copied_offer = copy.copy(offer)
        copied_offer.offer_id = offer_id
        self.__insert_into_offers_basic(copied_offer)
        self.__insert_into_offers_by_city_and_address(copied_offer)

        if copied_offer.company_name:
            self.__insert_into_offers_by_company_name(copied_offer)
        self.__insert_into_offers_by_city_and_price(copied_offer)
        return copied_offer

    def __insert_into_offers_by_city_and_address(self, offer: Offer):
        query = "INSERT INTO offers_by_city_and_street (address_city, address_street, offer_id, title, price, area, status, owner_id, apartment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.session.execute(query, (
            offer.address_city, offer.address_street, offer.offer_id, offer.title, offer.price, offer.area,
            offer.status,
            offer.owner_id, offer.apartment_id))

    def __insert_into_offers_by_city_and_price(self, offer: Offer):
        query = "INSERT INTO offers_by_city_and_price (address_city, address_street, price, offer_id, title, area, status, owner_id, apartment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.session.execute(query, (
            offer.address_city, offer.address_street, offer.price, offer.offer_id, offer.title, offer.area,
            offer.owner_id, offer.status,
            offer.apartment_id))

    def __insert_into_offers_by_company_name(self, offer: Offer):
        query = "INSERT INTO offers_by_company_name (company_name, offer_id, title, price, area, status, owner_id, apartment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.session.execute(query, (
            offer.company_name, offer.offer_id, offer.title, offer.price, offer.area, offer.status, offer.owner_id,
            offer.apartment_id))

    def __insert_into_offers_basic(self, offer):
        query = "INSERT INTO offers_basic (offer_id, address_city, address_street, company_name, price) VALUES (%s, %s, %s, %s, %s)"
        self.session.execute(query, (
            offer.offer_id, offer.address_city, offer.address_street, offer.company_name, offer.price))

    def update(self, offer: Offer):
        self.__update_offers_by_city_and_address(offer)
        self.__update_offers_by_city_and_price(offer)
        if offer.company_name:
            self.__update_offers_by_company_name(offer)

    def __update_offers_by_city_and_address(self, offer: Offer):
        query = "UPDATE offers_by_city_and_street SET title=%s, price=%s, area=%s, status=%s, owner_id=%s, apartment_id=%s WHERE address_city=%s AND address_street=%s AND offer_id=%s"
        self.session.execute(query, (
            offer.title, offer.price, offer.area, offer.status, offer.owner_id, offer.apartment_id, offer.address_city,
            offer.address_street, convert_text_into_uuid(offer.offer_id)))

    def __update_offers_by_company_name(self, offer: Offer):
        query = "UPDATE offers_by_company_name SET title=%s, price=%s, area=%s, status=%s, owner_id=%s, apartment_id=%s WHERE company_name=%s AND offer_id=%s"
        self.session.execute(query, (
            offer.title, offer.price, offer.area, offer.status, offer.owner_id, offer.apartment_id, offer.company_name,
            convert_text_into_uuid(offer.offer_id)))

    def __update_offers_by_city_and_price(self, offer: Offer):
        query = "UPDATE offers_by_city_and_price SET title=%s, area=%s, status=%s, owner_id=%s, apartment_id=%s WHERE address_city=%s AND price=%s AND offer_id=%s"
        self.session.execute(query, (
            offer.title, offer.area, offer.status, offer.owner_id, offer.apartment_id, offer.address_city,
            offer.price, convert_text_into_uuid(offer.offer_id)))

    def __map_from_row(self, single_row) -> Offer:
        return Offer(single_row.address_city,
                     single_row.address_street,
                     convert_uuid_into_text(single_row.offer_id),
                     single_row.title if hasattr(single_row, 'title') else None,
                     single_row.price,
                     single_row.area if hasattr(single_row, 'area') else None,
                     single_row.status if hasattr(single_row, 'status') else None,
                     single_row.owner_id if hasattr(single_row, 'owner_id') else None,
                     single_row.apartment_id if hasattr(single_row, 'apartment_id') else None,
                     single_row.company_name if hasattr(single_row, 'company_name') else None
                     )

    def __map_from_rows(self, rows) -> List[Offer]:
        return [self.__map_from_row(row) for row in rows]

    # Example usage
    def __map_average_price(self, row) -> ApartmentOfferAveragePrice:
        return ApartmentOfferAveragePrice(city=row.address_city,
                                          avg_price=row.avg_price,
                                          avg_price_per_m2=row.avg_price_per_m2
                                          )


    def __map_company_statistic(self, row) -> CompanyStatisticResult:
        return CompanyStatisticResult(company_name=row.company_name,
                                      avg_price=row.avg_price,
                                      avg_price_per_m2=row.avg_price_per_m2,
                                      sales_offer_count=row.sales_offer_count
                                      )

#
#
# repository = CassandraOfferRepository("market_app", "offers_by_city_and_street")
#
# row = repository.get_offers_by_city_and_address('Kraków', 'Krakowska')
#
# #
# # # Insert a new row
# # repository.insert("New York", "123 Main St", 456, "New Offer", 1000, 500, 1, 2)
# #
# # # Update an existing row
# # repository.update(offer_id, "Updated Offer", 1500)
#
# offer = Offer("New York", "Fifth Avenue", '31f72b98-8b75-11ed-afb3-78b58af1d5d7', "Luxury apartment2", 1000000.0, 50.0,
#               1, 1, "MAIN_COMPANY")
# repository.update(offer)
