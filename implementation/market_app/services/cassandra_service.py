import typing as t

from fastapi import HTTPException, status

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    ApartmentOfferAveragePrice, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentInfo, FullApartment, OwnerApiModel, \
    CompanyStatisticResult
from market_app.models.db_models.cassandra_models import Apartment, Offer
from market_app.repositories.cassandra.cassandra_address_repository import CassandraAddressRepository
from market_app.repositories.cassandra.cassandra_apartment_repository import CassandraApartmentRepository
from market_app.repositories.cassandra.cassandra_offer_repository import CassandraOfferRepository
from market_app.repositories.cassandra.cassandra_owner_repository import CassandraOwnerRepository
from market_app.repositories.repository_dependencies import get_cassandra_session
from market_app.services.reader_interface import ISalesReader
from market_app.services.mapper.cassandra_mappers import CassandraMapper


class CassandraService(ISalesReader):

    def __init__(self):
        session = get_cassandra_session()
        self.cassandra_owner_repository = CassandraOwnerRepository(session)
        self.cassandra_apartment_repository = CassandraApartmentRepository(session)
        self.cassandra_offer_repository = CassandraOfferRepository(session)
        self.cassandra_address_repository = CassandraAddressRepository(session)

    def create_apartment_with_dependencies(self, apartment: FullApartment) -> FullApartment:
        owner_id = apartment.owner.owner_id
        if not owner_id:
            owner = self.cassandra_owner_repository.insert(apartment.owner)
            owner_id = owner.owner_id
        else:
            owner = self.cassandra_owner_repository.get_by_id(owner_id)

        address_id = apartment.address.address_id
        if not address_id:
            address = self.cassandra_address_repository.insert(apartment.address)
            address_id = address.address_id
        else:
            address = self.cassandra_address_repository.find_by_id(address_id)

        apartment_entity = CassandraMapper.apartment_info_to_apartment(apartment.apartment, owner_id, address_id)
        saved_apartment: Apartment = self.cassandra_apartment_repository.insert(apartment_entity)

        saved_offers: [] = []
        for single_offer in apartment.offers:
            mapped_offer = CassandraMapper.map_sales_offer_to_offer(single_offer,
                                                                    saved_apartment,
                                                                    owner,
                                                                    address)
            saved_single_offer = self.cassandra_offer_repository.insert(mapped_offer)
            saved_offers.append(saved_single_offer)

        return FullApartment(apartment=CassandraMapper.apartment_to_apartment_info(saved_apartment),
                             owner=owner,
                             address=address,
                             offers=CassandraMapper.map_offers_to_api_models(saved_offers))

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> t.List[ApartmentOfferSearchResult]:
        offers = self.cassandra_offer_repository.get_offers_by_city_and_price_range(
            query.city,
            query.min_price,
            query.max_price
        )
        return list(map(lambda x: CassandraMapper.map_offer_to_apartment_for_sale_result(x), offers))

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        self.cassandra_offer_repository.delete(offer_id)

    def update_apartment(self, apartment_id: str, update_info: ApartmentUpdateInfo) -> ApartmentInfo:
        curr_apartment = self.cassandra_apartment_repository.get_by_id(apartment_id)
        if not curr_apartment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Apartment with id: {apartment_id} couldn\'t be found')

        updated_apartment = CassandraMapper.apartment_update_to_apartment(update_info, curr_apartment)
        self.cassandra_apartment_repository.update(updated_apartment)
        print(updated_apartment.apartment_id)
        return CassandraMapper.apartment_to_apartment_info(updated_apartment)

    def update_sale_offer_status(self, offer_id: str, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        offer_basic = self.cassandra_offer_repository.get_offer_basic_by_id(offer_id)
        if not offer_basic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Offer with id: {offer_id} couldn\'t be found')
        offer_full = self.cassandra_offer_repository.get_offers_by_city_and_price_and_id(offer_basic.address_city,
                                                                                         offer_basic.price,
                                                                                         offer_basic.offer_id)
        offer_full.status = update_info.status
        self.cassandra_offer_repository.update(offer_full)
        return CassandraMapper.map_offer_to_api_model(offer_full)

    def get_average_apartment_prices_by_city(self, city: str) -> t.List[ApartmentOfferAveragePrice]:
        return self.cassandra_offer_repository.get_average_price_by_city(city)

    def get_companies_sales_statistics(self, company_name: str) -> t.List[CompanyStatisticResult]:
        return self.cassandra_offer_repository.get_statistic_by_company(company_name)

    def find_apartment_by_id(self, apartment_id: str) -> ApartmentInfo:
        apartment = self.cassandra_apartment_repository.get_by_id(apartment_id)
        if not apartment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Apartment with id: {apartment_id} couldn\'t be found')

        return CassandraMapper.apartment_to_apartment_info(apartment)

    def get_owner_by_id(self, owner_id: str) -> OwnerApiModel:
        owner = self.cassandra_owner_repository.get_by_id(owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Owner with id: {owner_id} couldn\'t be found')

        return CassandraMapper.map_owner_to_api_model(owner)

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        offers: t.List[Offer] = self.cassandra_offer_repository.get_offers_by_city_and_address(query.city,
                                                                                               query.street_name)
        return list(map(lambda x: CassandraMapper.map_offer_to_apartment_for_sale_result(x), offers))
