import typing as t

from bson import ObjectId
from fastapi import HTTPException, status

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    ApartmentSearchQuery, ApartmentOfferAveragePrice, ApartmentPriceByDistrict, SaleOfferStatusUpdate, SaleOffer, \
    ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, FullApartment, OwnerApiModel, CompanyStatisticResult, ApartmentInfo
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
            owner_entity = MongoDbMapper.map_owner_api_model_to_owner_model(apartment.owner)
            owner_id = self.mongo_db_owner_repository.create(owner_entity)
            owner_entity.id = owner_id
        else:
            owner_entity = MongoDbMapper.map_owner_model_to_owner_api_model(
                self.mongo_db_owner_repository.get_by_id(owner_id)
            )

        address_id = apartment.address.address_id
        if not address_id:
            address_entity = MongoDbMapper.map_address_to_address_model(apartment.address)
            address_id = self.mongo_db_address_repository.create(address_entity)
            address_entity.id = address_id
        else:
            address_entity = MongoDbMapper.map_address_model_to_address(
                self.mongo_db_address_repository.get_by_id(address_id)
            )

        apartment_entity = MongoDbMapper.map_apartment_info_to_model(
            apartment.apartment, owner_id, address_id
        )
        saved_apartment_id = self.mongo_db_apartment_repository.create(apartment_entity)
        apartment_entity.id = saved_apartment_id

        saved_offers: [] = []
        for single_offer in apartment.offers:
            mapped_offer = MongoDbMapper.map_sale_offer_to_offer_model(single_offer,
                                                                       apartment_entity,
                                                                       owner_entity,
                                                                       address_entity)
            saved_single_offer_id = self.mongo_db_offer_repository.create(mapped_offer)
            mapped_offer.id = saved_single_offer_id
            saved_offers.append(mapped_offer)

        return FullApartment(apartment=MongoDbMapper.map_apartment_model_to_info(apartment_entity),
                             owner=MongoDbMapper.map_owner_model_to_owner_api_model(owner_entity),
                             address=MongoDbMapper.map_address_model_to_address(address_entity),
                             offers=MongoDbMapper.map_offer_models_to_sale_offers(saved_offers))

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> t.List[ApartmentOfferSearchResult]:
        offers = self.mongo_db_offer_repository.get_offers_by_city_and_price_range(
            query.city, query.min_price, query.max_price
        )
        return MongoDbMapper.map_offers_models_to_search_results(offers)

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        self.mongo_db_offer_repository.delete(offer_id)

    def update_apartment(self, apartment_id: str, update_info: ApartmentUpdateInfo) -> ApartmentInfo:
        mapped_entity = MongoDbMapper.map_apartment_update_info_to_apartment_model(update_info)
        mapped_entity.id = ObjectId(apartment_id)
        self.mongo_db_apartment_repository.update(mapped_entity)
        return MongoDbMapper.map_apartment_model_to_info(mapped_entity)

    def update_sale_offer_status(self, offer_id: str, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        offer_entity = self.mongo_db_offer_repository.get_by_id(offer_id)
        if not offer_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Offer with id: {offer_id} couldn\'t be found')

        offer_entity.status = update_info.status
        self.mongo_db_offer_repository.update(offer_entity)
        return MongoDbMapper.map_offer_model_to_sale_offer(offer_entity)

    def get_average_apartment_prices_by_city(self, city: str) -> t.List[ApartmentOfferAveragePrice]:
        return self.mongo_db_offer_repository.get_average_price_by_city(city)

    def get_companies_sales_statistics(self, company_name: str) -> t.List[CompanyStatisticResult]:
        return self.mongo_db_offer_repository.get_companies_sales_statistics(company_name)

    def find_apartment_by_id(self, apartment_id: str) -> ApartmentInfo:
        apartment_entity = self.mongo_db_apartment_repository.get_by_id(apartment_id)
        if not apartment_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Apartment with id: {apartment_id} couldn\'t be found')

        return MongoDbMapper.map_apartment_model_to_info(apartment_entity)

    def get_owner_by_id(self, owner_id: str) -> OwnerApiModel:
        owner_entity = self.mongo_db_owner_repository.get_by_id(owner_id)
        if not owner_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Owner with id: {owner_id} couldn\'t be found')
        return MongoDbMapper.map_owner_model_to_owner_api_model(owner_entity)

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        offers = self.mongo_db_offer_repository.get_offers_by_city_and_address(
            query.city, query.street_name
        )
        return MongoDbMapper.map_offers_models_to_search_results(offers)
