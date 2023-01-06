import typing as t

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    CompanyAndApartments, ApartmentSearchQuery, ApartmentSearchResult, ApartmentSaleOffersByStatusQuery, \
    ApartmentSaleOffersByStatus, ApartmentPriceByDistrict, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, ApartmentInfo, FullApartment
from market_app.services.reader_interface import ISalesReader


class MongoDbReader(ISalesReader):
    def create_apartment_with_dependencies(self, apartment: FullApartment) -> None:
        pass

    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
        pass

    def delete_apartment_sale_offer(self, offer_id: str) -> None:
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
        pass

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        print("Mongo Called")
        pass