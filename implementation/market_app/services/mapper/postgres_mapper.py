import datetime

from implementation.market_app.models.api_models import ApartmentOfferSearchResult, ApartmentUpdateInfo, SaleOffer, \
    OwnerApiModel, ApartmentInfo
from implementation.market_app.models.db_models.postgres_models import Offer, Apartment, Owner, Address


class PostgresMapper:

    @staticmethod
    def map_offer_to_apartment_for_sale_result(offer: Offer) -> ApartmentOfferSearchResult:
        return ApartmentOfferSearchResult(
            offer_id=offer.offer_id,
            apartment_id=offer.apartment_id,
            city=offer.address_city,
            street=offer.address_street,
            price=offer.price,
            is_negotiable=False,
            title=offer.title,
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
    def apartment_to_apartment_info(cls, updated_apartment):
        pass

    @staticmethod
    def map_offer_to_api_model(offer: Offer) -> SaleOffer:
        creation_date = datetime.now()
        return SaleOffer(
            creation_date=creation_date,
            price=offer.price,
            is_negotiable=False,
            title=offer.title,
            status=offer.status,
            modification_date=None,
            description=None,
            agency_fee=None
        )

    @staticmethod
    def map_owner_to_api_model(owner: Owner) -> OwnerApiModel:
        return OwnerApiModel(
            owner_id=owner.owner_id,
            name=owner.name,
            surname=owner.surname,
            phone_number=owner.phone_number,
            address=owner.address,
            email_address=owner.email_address,
            company_name=owner.company_name
        )

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
            apartment_id="",
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
    def map_sales_offer_to_offer(sales_offer: SaleOffer, apartment: Apartment, owner: Owner, address: Address):
        return Offer(
            address_city=address.city,
            address_street=address.street_name,
            offer_id="",
            title=sales_offer.title,
            price=sales_offer.price,
            area=apartment.area,
            owner_id=owner.owner_id,
            apartment_id=apartment.apartment_id,
            company_name=owner.company_name,
            status=sales_offer.status
        )