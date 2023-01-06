from datetime import datetime
from typing import List

from market_app.models.api_models import ApartmentInfo, SaleOffer, ApartmentForSaleSearchResult
from market_app.models.db_models.cassandra_models import Apartment, Offer, Address, Owner


class CassandraMapper:

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
            company_name=owner.company_name
        )

    @staticmethod
    def apartment_to_apartment_info(apartment: Apartment):
        return ApartmentInfo(
            apartment_id=apartment.apartment_id,
            area=apartment.area,
            creation_year=apartment.creation_year,
            last_renovation_year=apartment.last_renovation_year,
            building_type=apartment.building_type,
            heating_type=apartment.heating_type,
            furnished=apartment.is_furnished,
            rooms_count=apartment.rooms_count
        )

    # TODO - dodać do modelu BD reszte info
    @staticmethod
    def map_offers_to_api_models(offers: List[Offer]) -> List[SaleOffer]:
        return list(map(lambda x: CassandraMapper.map_offer_to_api_model(x), offers))

    @staticmethod
    def map_offer_to_api_model(offer: Offer) -> SaleOffer:
        creation_date = datetime.now()
        return SaleOffer(
            creation_date=creation_date,
            price=offer.price,
            is_negotiable=False,
            title=offer.title,
            status='active',
            modification_date=None,
            description=None,
            agency_fee=None
        )

    @staticmethod
    def map_offer_to_apartment_for_sale_result(offer: Offer) -> ApartmentForSaleSearchResult:
        return ApartmentForSaleSearchResult(
            offer_id=offer.offer_id,
            city=offer.address_city,
            street=offer.address_street,
            price=offer.price,
            is_negotiable=False,
            title=offer.title,
            status="active"
        )
