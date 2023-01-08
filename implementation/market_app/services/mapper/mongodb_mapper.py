import datetime
from typing import List

from bson import ObjectId

from market_app.models.api_models import OwnerApiModel, Address, SaleOffer, ApartmentInfo, ApartmentOfferSearchResult
from market_app.models.db_models.fast_api_mongodb_models import OwnerModel, AddressModel, OfferModel, ApartmentModel, \
    PyObjectId


class MongoDbMapper:

    @staticmethod
    def map_owner_api_model_to_owner_model(api_model: OwnerApiModel) -> OwnerModel:
        return OwnerModel(
            id=ObjectId() if not api_model.owner_id else api_model.owner_id,
            name=api_model.name,
            surname=api_model.surname,
            phone_number=api_model.phone_number,
            address=api_model.address,
            email_address=api_model.email_address,
            company_name=api_model.company_name if api_model.company_name else ''
        )

    @staticmethod
    def map_owner_model_to_owner_api_model(model: OwnerModel) -> OwnerApiModel:
        return OwnerApiModel(
            owner_id=str(model.id),
            name=model.name,
            surname=model.surname,
            phone_number=model.phone_number,
            address=model.address,
            email_address=model.email_address,
            company_name=model.company_name if model.company_name else ''
        )

    @staticmethod
    def map_address_to_address_model(address: Address) -> AddressModel:
        return AddressModel(
            id=ObjectId() if not address.address_id else address.address_id,
            city=address.city,
            street_name=address.street_name,
            building_nr=address.building_nr,
            apartment_nr=address.apartment_nr,
            postal_code=address.postal_code,
        )

    @staticmethod
    def map_address_model_to_address(address_model: AddressModel) -> Address:
        return Address(
            address_id=str(address_model.id),
            city=address_model.city,
            street_name=address_model.street_name,
            building_nr=address_model.building_nr,
            apartment_nr=address_model.apartment_nr,
            postal_code=address_model.postal_code,
        )

    @staticmethod
    def map_sale_offer_to_offer_model(sale_offer: SaleOffer,
                                      apartment: ApartmentModel,
                                      owner: OwnerModel,
                                      address: AddressModel) -> OfferModel:
        return OfferModel(
            address={
                "id": str(address.id),
                "city": address.city,
                "street": address.street_name,
            },
            price=sale_offer.price,
            title=sale_offer.title,
            area=apartment.area,
            owner={
                "id": str(owner.id),
                "company_name": owner.company_name if owner.company_name else ''
            },
            apartment_id=str(apartment.id),
            creation_date=sale_offer.creation_date,
            modification_date=sale_offer.modification_date if sale_offer.modification_date else sale_offer.creation_date,
            status=sale_offer.status,
            description=sale_offer.description,
            agency_fee=sale_offer.agency_fee,
            negotiable=sale_offer.is_negotiable
        )

    @staticmethod
    def map_offer_model_to_sale_offer(offer_model: OfferModel) -> SaleOffer:
        return SaleOffer(
            creation_date=offer_model.creation_date,
            price=offer_model.price,
            is_negotiable=offer_model.negotiable,
            title=offer_model.title,
            status=offer_model.status,
            modification_date=offer_model.modification_date,
            description=offer_model.description,
            agency_fee=offer_model.agency_fee
        )

    @staticmethod
    def map_offer_models_to_sale_offers(offer_models: List[OfferModel]) -> List[SaleOffer]:
        return list(map(lambda x: MongoDbMapper.map_offer_model_to_sale_offer(x), offer_models))

    @staticmethod
    def map_apartment_model_to_info(apartment_model: ApartmentModel) -> ApartmentInfo:
        return ApartmentInfo(
            apartment_id=str(apartment_model.id),
            area=apartment_model.area,
            creation_year=apartment_model.creation_year,
            last_renovation_year=apartment_model.last_renovation_year,
            building_type=apartment_model.building_type,
            heating_type=apartment_model.heating_type,
            furnished=apartment_model.is_furnished,
            rooms_count=apartment_model.rooms_count,
            address_id=str(apartment_model.address_id),
            owner_id=str(apartment_model.owner_id),
        )

    @staticmethod
    def map_apartment_info_to_model(apartment_info: ApartmentInfo, owner_id: str, address_id: str) -> ApartmentModel:
        return ApartmentModel(
            area=apartment_info.area,
            creation_year=apartment_info.creation_year,
            last_renovation_year=apartment_info.last_renovation_year,
            building_type=apartment_info.building_type,
            heating_type=apartment_info.heating_type,
            is_furnished=apartment_info.furnished,
            rooms_count=apartment_info.rooms_count,
            address_id=address_id,
            owner_id=owner_id
        )

    @staticmethod
    def map_offer_model_to_search_result(offer_model: OfferModel) -> ApartmentOfferSearchResult:
        return ApartmentOfferSearchResult(
            offer_id=str(offer_model.id),
            apartment_id=str(offer_model.apartment_id),
            city=offer_model.address['city'],
            street=offer_model.address['street'],
            price=offer_model.price,
            is_negotiable=offer_model.negotiable,
            title=offer_model.title,
            status=offer_model.status
        )

    @staticmethod
    def map_offers_models_to_search_results(offer_models: List[OfferModel]) -> List[ApartmentOfferSearchResult]:
        return list(map(lambda x: MongoDbMapper.map_offer_model_to_search_result(x), offer_models))
