import typing as t

from market_app.models.api_models import CompanyAndApartments, ApartmentSearchQuery, ApartmentSearchResult, \
    ApartmentSaleOffersByStatusQuery, ApartmentSaleOffersByStatus, ApartmentPriceByDistrict, SaleOfferStatusUpdate, \
    SaleOffer, ApartmentUpdateInfo, ApartmentPriceRangeQuery, ApartmentPriceRange, ApartmentInfo, \
    ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, FullApartment
from market_app.services.reader_interface import ISalesReader
from market_app.services.cassandra_service import CassandraService
from market_app.services.mongo_db_reader import MongoDbReader
from market_app.services.reader_options import ReaderOptions
import collections

TYPE_TO_CLASS_MAP = collections.ChainMap(
    {ReaderOptions.CASSANDRA: CassandraService},
    {ReaderOptions.MONGO_DB: MongoDbReader}
)


class ReaderManager(ISalesReader):
    def __init__(self, reader_type: ReaderOptions) -> None:
        self.reader_type = reader_type
        self.cassandra_reader = CassandraService()
        self.mongo_reader = MongoDbReader()
        self.__resolve_reader()
        pass

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        return self.current_reader.search_apartments_for_sale(query)

    def create_apartment_with_dependencies(self, apartment: FullApartment) -> None:
        return self.current_reader.create_apartment_with_dependencies(apartment)

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> t.List[ApartmentOfferSearchResult]:
        return self.current_reader.get_offers_by_city_and_price_range(query)

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        return self.current_reader.delete_apartment_sale_offer(offer_id)

    def update_apartment(self, apartment_id: int, update_info: ApartmentUpdateInfo) -> None:
        return self.current_reader.update_apartment(apartment_id, update_info)

    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        return self.current_reader.update_sale_offer_status(offer_id, update_info)

    def get_average_apartment_prices_by_city_and_street(self, city: str, street_name: str) -> ApartmentPriceByDistrict:
        return self.current_reader.get_average_apartment_prices_by_city_and_street(city, street_name)

    def get_apartment_sale_offers_by_status(self, query: ApartmentSaleOffersByStatusQuery) -> t.List[
        ApartmentSaleOffersByStatus]:
        return self.current_reader.get_apartment_sale_offers_by_status(query)

    def search_apartments(self, query: ApartmentSearchQuery) -> t.List[ApartmentSearchResult]:
        return self.current_reader.search_apartments(query)

    def get_companies_and_apartments(self) -> t.List[CompanyAndApartments]:
        return self.current_reader.get_companies_and_apartments()

    def __resolve_reader(self):
        if self.reader_type == ReaderOptions.CASSANDRA:
            self.current_reader = self.cassandra_reader
        elif self.reader_type == ReaderOptions.MONGO_DB:
            self.current_reader = self.mongo_reader
        else:
            raise Exception("Unsupported state, no reader choosen")

    def change_reader(self, reader_type: ReaderOptions):
        self.reader_type = reader_type
        self.__resolve_reader()


if __name__ == "__main__":
    reader_manager = ReaderManager(ReaderOptions.CASSANDRA)

    query = ApartmentForSaleSearchQuery(city='Warsaw', address='ul. Marszałkowska')

    reader_manager.search_apartments_for_sale(query=query)
    reader_manager.change_reader(ReaderOptions.MONGO_DB)
    reader_manager.search_apartments_for_sale(query)


READER_MANAGER = ReaderManager(ReaderOptions.CASSANDRA)
