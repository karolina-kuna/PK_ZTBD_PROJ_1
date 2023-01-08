import typing as t

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    ApartmentSearchQuery, ApartmentOfferAveragePrice, ApartmentPriceByDistrict, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, FullApartment, OwnerApiModel, CompanyStatisticResult
from market_app.repositories.mongo_db.mongo_db_address_repository import MongoDbAddressRepository
from market_app.repositories.mongo_db.mongo_db_apartment_repository import MongoDbApartmentRepository
from market_app.repositories.mongo_db.mongo_db_offer_repository import MongoDbOfferRepository
from market_app.repositories.mongo_db.mongo_db_owner_repository import MongoDbOwnerRepository
from market_app.repositories.repository_dependencies import get_mongo_db_db
from market_app.services.mapper.mongodb_mapper import MongoDbMapper
from market_app.services.reader_interface import ISalesReader



class MongoDbService(ISalesReader):
    def __init__(self):
        database = get_mongo_db_db()
        self.mongo_db_owner_repository = MongoDbOwnerRepository(database)
        self.mongo_db_apartment_repository = MongoDbApartmentRepository(database)
        self.mongo_db_offer_repository = MongoDbOfferRepository(database)
        self.mongo_db_address_repository = MongoDbAddressRepository(database)

    def create_apartment_with_dependencies(self, apartment: FullApartment) -> FullApartment:
        owner_id = apartment.owner.owner_id
        if not owner_id:
            owner_model = MongoDbMapper.map_owner_api_model_to_owner_model(apartment.owner)
            owner_id = self.mongo_db_owner_repository.create(owner_model)
        else:
            owner = MongoDbMapper.map_owner_model_to_owner_api_model(
                self.mongo_db_owner_repository.get_by_id(owner_id)
            )

        address_id = apartment.address.address_id
        if not address_id:
            address = self.mongo_db_address_repository.insert(apartment.address)
            address_id = address.address_id
        else:
            address = self.mongo_db_address_repository.find_by_id(address_id)

        apartment_entity = MongoDbMapper.apartment_info_to_apartment(apartment.apartment, owner_id, address_id)
        saved_apartment: Apartment = self.cassandra_apartment_repository.insert(apartment_entity)

        saved_offers: [] = []
        for single_offer in apartment.offers:
            mapped_offer = MongoDbMapper.map_sales_offer_to_offer(single_offer,
                                                                    saved_apartment,
                                                                    owner,
                                                                    address)
            saved_single_offer = self.cassandra_offer_repository.insert(mapped_offer)
            saved_offers.append(saved_single_offer)

        return FullApartment(apartment=CassandraMapper.apartment_to_apartment_info(saved_apartment),
                             owner=owner,
                             address=address,
                             offers=CassandraMapper.map_offers_to_api_models(saved_offers))

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
        pass

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        pass

    def update_apartment(self, apartment_id: int, update_info: ApartmentUpdateInfo) -> None:
        pass

    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        pass

    def get_average_apartment_prices_by_city(self, city: str, street_name: str) -> ApartmentPriceByDistrict:
        pass

    def get_companies_sales_statistics(self, company_name: str) -> t.List[CompanyStatisticResult]:
        pass

    def find_apartment_by_id(self, query: ApartmentSearchQuery) -> t.List[ApartmentOfferAveragePrice]:
        pass

    def get_owner_by_id(self, owner_id: str) -> OwnerApiModel:
        pass

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        print("Mongo Called")
        pass
