from abc import ABC, abstractmethod
import typing as t

from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentOfferSearchResult, \
    CompanyAndApartments, ApartmentSearchQuery, ApartmentOfferAveragePrice, ApartmentSaleOffersByStatusQuery, \
    ApartmentSaleOffersByStatus, SaleOfferStatusUpdate, ApartmentUpdateInfo, ApartmentPriceRangeQuery, \
    ApartmentPriceRange, ApartmentInfo, SaleOffer, ApartmentPriceByDistrict, FullApartment, OwnerApiModel, \
    CompanyStatisticResult


class ISalesReader(ABC):

    @abstractmethod
    def search_apartments_for_sale(self, query: ApartmentForSaleSearchQuery) -> t.List[ApartmentOfferSearchResult]:
        pass

    @abstractmethod
    def create_apartment_with_dependencies(self, full_apartment: FullApartment) -> None:
        pass

    @abstractmethod
    def get_offers_by_city_and_price_range(self, query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
        pass

    @abstractmethod
    def delete_apartment_sale_offer(self, offer_id: str) -> None:
        pass

    @abstractmethod
    def update_apartment(self, apartment_id: str, update_info: ApartmentUpdateInfo) -> ApartmentInfo:
        pass

    @abstractmethod
    def update_sale_offer_status(self, offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
        pass

    @abstractmethod
    def get_average_apartment_prices_by_city(self, city: str) -> t.List[ApartmentOfferAveragePrice]:
        pass

    @abstractmethod
    def get_companies_sales_statistics(self, company_name: str) -> t.List[CompanyStatisticResult]:
        pass

    @abstractmethod
    def find_apartment_by_id(self, apartment_id: str) -> ApartmentInfo:
        pass

    @abstractmethod
    def get_owner_by_id(self, owner_id: str) -> OwnerApiModel:
        pass
