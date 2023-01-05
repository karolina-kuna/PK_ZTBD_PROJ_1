import typing as t

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentForSaleSearchResult, \
    CompanyAndApartments, ApartmentSearchQuery, ApartmentSearchResult, ApartmentSaleOffersByStatusQuery, \
    ApartmentSaleOffersByStatus, ApartmentPriceByDistrict, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, ApartmentInfo
from market_app.services.reader_interface import ISalesReader


class MongoDbReader(ISalesReader):
    def add_apartment_info(self, apartment_id: int, apartment_info: ApartmentInfo) -> None:
        pass

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
        pass

    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentForSaleSearchResult]:
        print("Mongo Called")
        pass