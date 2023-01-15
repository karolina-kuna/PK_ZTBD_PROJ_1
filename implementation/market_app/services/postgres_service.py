import typing as t
from abc import ABC

from fastapi import HTTPException, status

from implementation.market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    FullApartment, ApartmentPriceRangeQuery, ApartmentUpdateInfo, ApartmentInfo, \
    SaleOfferStatusUpdate, ApartmentOfferAveragePrice, CompanyStatisticResult, OwnerApiModel, SaleOffer
from implementation.market_app.models.postgres_models import Apartment, Offer
from implementation.market_app.repositories.postgres_repository.postgres_address_repository import \
    PostgresAddressRepository
from implementation.market_app.repositories.postgres_repository.postgres_apartment_repository import \
    PostgresApartmentRepository
from implementation.market_app.repositories.postgres_repository.postgres_offer_repository import PostgresOfferRepository
from implementation.market_app.repositories.postgres_repository.postgres_owner_repository import PostgresOwnerRepository
from implementation.market_app.services.mapper.postgres_mapper import PostgresMapper
from implementation.market_app.services.reader_interface import ISalesReader
from implementation.parser.data_generator import apartment


class PostgresSQLService(ISalesReader, ABC):

    def __init__(self):
        self.postgres_owner_repository = PostgresOwnerRepository()
        self.postgres_apartment_repository = PostgresApartmentRepository()
        self.postgres_offer_repository = PostgresOfferRepository()
        self.postgres_address_repository = PostgresAddressRepository()

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        offers = self.postgres_offer_repository.get_offers_by_city_and_address(query.city, query.street_name)
        return list(map(lambda x: PostgresMapper.map_offer_to_apartment_for_sale_result(x), offers))

    def create_apartment_with_dependencies(self, full_apartment: FullApartment) -> FullApartment:
        owner_id = apartment.owner_id
        if not owner_id:
            owner = self.postgres_owner_repository.insert(apartment.owner_id)
            owner_id = owner.owner_id
        else:
            owner = self.postgres_owner_repository.get_by_id(owner_id)

        address_id = apartment.address.address_id
        if not address_id:
            address = self.postgres_address_repository.insert(apartment.address)
            address_id = address.address_id
        else:
            address = self.postgres_address_repository.find_by_id(address_id)

        apartment_entity = PostgresMapper.apartment_info_to_apartment(apartment.apartment, owner_id, address_id)
        saved_apartment: Apartment = self.postgres_apartment_repository.insert(apartment_entity)

        saved_offers: [] = []
        for single_offer in apartment.offers:
            mapped_offer = PostgresMapper.map_sales_offer_to_offer(single_offer,
                                                                   saved_apartment,
                                                                   owner,
                                                                   address)
            saved_single_offer = self.postgres_offer_repository.insert(mapped_offer)
            saved_offers.append(saved_single_offer)

        return FullApartment(apartment=PostgresMapper.apartment_to_apartment_info(saved_apartment),
                             owner=owner,
                             address=address,
                             offers=PostgresMapper.map_offers_to_api_models(saved_offers))

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> list[ApartmentOfferSearchResult]:
        offers = self.postgres_offer_repository.get_offers_by_city_and_price_range(
            query.city,
            query.min_price,
            query.max_price
        )
        return list(map(lambda x: PostgresMapper.map_offer_to_apartment_for_sale_result(x), offers))

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        self.postgres_offer_repository.delete(int(offer_id))

    def update_apartment(self, apartment_id: str, update_info: ApartmentUpdateInfo) -> ApartmentInfo:
        curr_apartment = self.postgres_apartment_repository.get_by_id(int(apartment_id))
        if not curr_apartment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Apartment with id: {apartment_id} couldn\'t be found')

        updated_apartment = PostgresMapper.apartment_update_to_apartment(update_info, curr_apartment)
        self.postgres_apartment_repository.update(updated_apartment,curr_apartment.apartment_id)
        return PostgresMapper.apartment_to_apartment_info(updated_apartment)

    # def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
    #     offer = self.postgres_offer_repository.get_by_id(int(offer_id))
    #     address_id = self.postgres_apartment_repository.get_by_id(offer.apartment_id).address_id
    #     city = self.postgres_address_repository.find_by_id(int(address_id)).city
    #     if not offer:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f'Offer with id: {offer_id} couldn\'t be found')
    #     offer_full = self.postgres_offer_repository.get_offers_by_city_and_price_and_id(city,
    #                                                                                     offer.price,
    #                                                                                     offer_id)
    #     offer_full[0].status = update_info.status
    #     self.postgres_offer_repository.update(offer_full[0])
    #     return PostgresMapper.map_offer_to_api_model(offer_full)

    def update_sale_offer_status(self, offer_id: str, update_info: SaleOfferStatusUpdate) -> Offer:
        return self.postgres_offer_repository.update_sale_offer_status(int(offer_id), update_info)

    def get_average_apartment_prices_by_city(self, city: str) -> t.List[ApartmentOfferAveragePrice]:
        return self.postgres_offer_repository.get_average_price_by_city(city)

    def get_companies_sales_statistics(self, company_name: str) -> t.List[CompanyStatisticResult]:
        return self.postgres_offer_repository.get_statistic_by_company(company_name)

    def find_apartment_by_id(self, apartment_id: str) -> ApartmentInfo:
        _apartment = self.postgres_apartment_repository.get_by_id(int(apartment_id))
        if not _apartment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Apartment with id: {apartment_id} couldn\'t be found')

        return PostgresMapper.apartment_to_apartment_info(_apartment)

    def get_owner_by_id(self, owner_id: str) -> OwnerApiModel:
        owner = self.postgres_owner_repository.get_by_id(int(owner_id))
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Owner with id: {owner_id} couldn\'t be found')

        return PostgresMapper.map_owner_to_api_model(owner)
