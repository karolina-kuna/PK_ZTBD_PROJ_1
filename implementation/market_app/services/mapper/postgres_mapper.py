import datetime
from typing import List

from implementation.market_app.models.api_models import ApartmentOfferSearchResult, ApartmentUpdateInfo, OwnerApiModel, \
    ApartmentInfo, SaleOffer

from implementation.market_app.models.postgres_models import Apartment, Owner, Address, Offer

from implementation.market_app.repositories.postgres_repository.postgres_address_repository import \
    PostgresAddressRepository


class PostgresMapper:

    @staticmethod
    def map_offer_to_apartment_for_sale_result(offer: Offer) -> ApartmentOfferSearchResult:
        repo = PostgresAddressRepository()
        address = repo.find_address_by_offer_id(offer.offer_id)
        return ApartmentOfferSearchResult(
            offer_id=offer.offer_id,
            apartment_id=offer.apartment_id,
            city=address.city,
            street='',
            price=offer.price,
            is_negotiable=False,
            title='',
            status=offer.status
        )

    @staticmethod
    def apartment_update_to_apartment(apartment_update: ApartmentUpdateInfo, apartment: Apartment):
        return Apartment(
            apartment_id=apartment.apartment_id,
            area=apartment_update.area if apartment_update.area else apartment.area,
            creation_year=apartment_update.creation_year if apartment_update.creation_year else apartment.creation_year,
            last_renovation_year=apartment_update.last_renovation_year if apartment_update.last_renovation_year else apartment.last_renovation_year,
            building_type=apartment_update.building_type if apartment_update.building_type else apartment.building_type,
            heating_type=apartment_update.heating_type if apartment_update.heating_type else apartment.heating_type,
            is_furnished=apartment_update.furnished if apartment_update.furnished else apartment.is_furnished,
            rooms_count=apartment_update.rooms_count if apartment_update.rooms_count else apartment.rooms_count,
            owner_id=apartment_update.owner_id if apartment_update.owner_id else apartment.owner_id,
            address_id=apartment_update.address_id if apartment_update.address_id else apartment.address_id
        )

    @staticmethod
    def map_offer_to_api_model(offer: Offer) -> SaleOffer:
        creation_date = datetime.date
        return SaleOffer(
            creation_date=creation_date,
            price=offer.price,
            is_negotiable=False,
            title=None,
            status=offer.status,
            modification_date=None,
            description=None,
            agency_fee=None
        )

    @staticmethod
    def map_owner_to_api_model(owner: Owner) -> OwnerApiModel:
        repo = PostgresAddressRepository()
        address = repo.find_address_by_owner_id(owner.owner_id)
        return OwnerApiModel(
            owner_id=owner.owner_id,
            name=owner.name,
            surname=owner.surname,
            phone_number=owner.phone_number,
            address=address.address_id,
            email_address=owner.email_address,
            company_name=owner.company_name
        )

    @staticmethod
    def map_offers_to_api_models(offers: List[Offer]) -> List[SaleOffer]:
        return list(map(lambda x: PostgresMapper.map_offer_to_api_model(x), offers))

    @staticmethod
    def apartment_to_apartment_info(apartment: Apartment) -> ApartmentInfo:
        return ApartmentInfo(
            apartment_id=apartment.apartment_id,
            area=apartment.area,
            creation_year=apartment.creation_year,
            last_renovation_year=apartment.last_renovation_year,
            building_type=apartment.building_type,
            heating_type=apartment.heating_type,
            furnished=apartment.is_furnished,
            rooms_count=apartment.rooms_count,
            owner_id=apartment.owner_id,
            address_id=apartment.address_id
        )

    @staticmethod
    def apartment_info_to_apartment(apartment_info: ApartmentInfo, owner_id: str, address_id: str) -> Apartment:
        return Apartment(
            apartment_id=None,
            area=apartment_info.area,
            creation_year=apartment_info.creation_year,
            last_renovation_year=apartment_info.last_renovation_year,
            building_type=apartment_info.building_type,
            heating_type=apartment_info.heating_type,
            is_furnished=apartment_info.furnished,
            rooms_count=apartment_info.rooms_count,
            owner_id=owner_id,
            address_id=address_id
        )

    @staticmethod
    def map_sales_offer_to_offer(sales_offer: Offer, apartment: Apartment, owner: Owner, address: Address):
        return SaleOffer(
            address_city=address.city,
            address_street=address.street_name,
            offer_id=None,
            title=None,
            price=sales_offer.price,
            area=apartment.area,
            owner_id=owner.owner_id,
            apartment_id=apartment.apartment_id,
            company_name=owner.company_name,
            status=sales_offer.status
        )
