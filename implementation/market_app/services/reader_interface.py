from abc import ABC, abstractmethod
import typing as t

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentForSaleSearchResult, \
    CompanyAndApartments, ApartmentSearchQuery, ApartmentSearchResult, ApartmentSaleOffersByStatusQuery, \
    ApartmentSaleOffersByStatus, SaleOfferStatusUpdate, ApartmentUpdateInfo, ApartmentPriceRangeQuery, \
    ApartmentPriceRange, ApartmentInfo, SaleOffer, ApartmentPriceByDistrict, FullApartment


class ISalesReader(ABC):

    @abstractmethod
    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentForSaleSearchResult]:
        pass

    @abstractmethod
    def create_apartment_with_dependencies(self, full_apartment: FullApartment) -> None:
        pass

    @abstractmethod
    def get_apartment_price_range(self, query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
        pass

    @abstractmethod
    def delete_apartment_sale_offer(self, apartment_id: int) -> None:
        pass

    @abstractmethod
    def update_apartment(self, apartment_id: int, update_info: ApartmentUpdateInfo) -> None:
        pass

    @abstractmethod
    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        pass

    @abstractmethod
    def get_average_apartment_prices_by_city_and_street(self, city: str, street_name: str) -> ApartmentPriceByDistrict:
        pass

    @abstractmethod
    def get_apartment_sale_offers_by_status(self, query: ApartmentSaleOffersByStatusQuery) -> t.List[ApartmentSaleOffersByStatus]:
        pass

    @abstractmethod
    def search_apartments(self, query: ApartmentSearchQuery) -> t.List[ApartmentSearchResult]:
        pass

    @abstractmethod
    def get_companies_and_apartments(self) -> t.List[CompanyAndApartments]:
        pass
