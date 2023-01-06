import typing as t

from cassandra.cluster import Cluster
from fastapi import Depends

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentForSaleSearchResult, \
    CompanyAndApartments, ApartmentSearchQuery, ApartmentSearchResult, ApartmentSaleOffersByStatusQuery, \
    ApartmentSaleOffersByStatus, ApartmentPriceByDistrict, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, ApartmentInfo, FullApartment, FullApartmentResponse
from market_app.models.db_models.cassandra_models import Apartment, Offer
from market_app.repositories.cassandra_address_repository import CassandraAddressRepository
from market_app.repositories.cassandra_apartment_repository import CassandraApartmentRepository
from market_app.repositories.cassandra_offer_repository import CassandraOfferRepository
from market_app.repositories.cassandra_owner_repository import CassandraOwnerRepository
from market_app.services.reader_interface import ISalesReader
from market_app.services.mapper.cassandra_mappers import CassandraMapper


class CassandraService(ISalesReader):

    def __init__(self):
        cluster = Cluster()
        self.cassandra_owner_repository = CassandraOwnerRepository(cluster)
        self.cassandra_apartment_repository = CassandraApartmentRepository(cluster)
        self.cassandra_offer_repository = CassandraOfferRepository(cluster)
        self.cassandra_address_repository = CassandraAddressRepository(cluster)

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

    def get_apartment_price_range(self, query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
        pass

    def delete_apartment_sale_offer(self, apartment_id: int) -> None:
        pass

    def update_apartment(self, apartment_id: int, update_info: ApartmentUpdateInfo) -> None:
        pass

    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        pass

    def get_average_apartment_prices_by_city_and_street(self, city: str, street_name: str) -> ApartmentPriceByDistrict:
        pass

    def get_apartment_sale_offers_by_status(self, query: ApartmentSaleOffersByStatusQuery) -> t.List[
        ApartmentSaleOffersByStatus]:
        pass

    def search_apartments(self, query: ApartmentSearchQuery) -> t.List[ApartmentSearchResult]:
        pass

    def get_companies_and_apartments(self) -> t.List[CompanyAndApartments]:
        return self.cassandra_owner_repository.get_all()

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentForSaleSearchResult]:
        offers: t.List[Offer] = self.cassandra_offer_repository.get_offers_by_city_and_address(query.city,
                                                                                               query.street_name)
        return list(map(lambda x: CassandraMapper.map_offer_to_apartment_for_sale_result(x), offers))
