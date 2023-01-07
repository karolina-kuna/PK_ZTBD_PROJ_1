import typing as t

from fastapi import APIRouter, HTTPException, status, Depends

from market_app.dependencies import get_reader_manager
from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentInfo, ApartmentOfferSearchResult, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceByDistrict, ApartmentSaleOffersByStatusQuery, ApartmentSaleOffersByStatus, ApartmentSearchQuery, \
    ApartmentOfferAveragePrice, CompanyAndApartments, FullApartment, OwnerApiModel, CompanyStatisticResult
from market_app.services.reader_manager import ReaderManager, READER_MANAGER

sales_router = APIRouter(prefix="/sales", tags=["Sales"])


# 1.	Wyszukiwanie mieszkania do kupna po mieście i adresie
# a.	Pobranie szczegółów dotyczących mieszkania
# b.	Pobranie szczegółów dotyczących właściciela
@sales_router.get("/apartments/for-sale/search")
def search_apartments_for_sale(city_name: str,
                               street_name: str,
                               ) -> t.List[ApartmentOfferSearchResult]:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.search_apartments_for_sale(
        ApartmentForSaleSearchQuery(city=city_name, street_name=street_name)
    )


@sales_router.post("/apartment-with-dependencies")
def add_apartment_info(apartment: FullApartment) -> None:
    reader_manager: ReaderManager = READER_MANAGER
    reader_manager.create_apartment_with_dependencies(apartment)


# 3.	Wyświetlenie informacji o przedziale informacjach cenowych w danej lokalizacji
@sales_router.get("/apartments/sale-offers/by-price-range")
def get_apartment_price_range(city: str, min_price: float, max_price: float) -> t.List[ApartmentOfferSearchResult]:
    query = ApartmentPriceRangeQuery(city=city, min_price=min_price, max_price=max_price)
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.get_offers_by_city_and_price_range(query)


# 4. Usunięcie oferty sprzedaży mieszkania
@sales_router.delete("/apartments/sale-offers/{offer_id}", status_code=status.HTTP_200_OK)
def delete_apartment_sale_offer(offer_id: str):
    reader_manager: ReaderManager = READER_MANAGER
    reader_manager.delete_apartment_sale_offer(offer_id)
    return {"offer_id": offer_id, "message": "Deleted successfully"}


# 5. Zmiana danych mieszkania
@sales_router.patch("/apartments/{apartment_id}")
def update_apartment(apartment_id: str, update_info: ApartmentUpdateInfo):
    reader_manager: ReaderManager = READER_MANAGER
    updated_apartment = reader_manager.update_apartment(apartment_id, update_info)
    return {"apartment": updated_apartment}


# 6. Zmiana statusu oferty kupna
@sales_router.patch("/apartments/sale-offers/{offer_id}/status")
def update_sale_offer_status(offer_id: str, update_info: SaleOfferStatusUpdate) -> SaleOffer:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.update_sale_offer_status(offer_id, update_info)


# 7. Wyszukanie średnich cen mieszkań na metr kwadratowy po dzielnicy
@sales_router.get("/statistics/average-prices")
def get_average_apartment_prices_by_city(city: t.Optional[str] = '') -> t.List[ApartmentOfferAveragePrice]:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.get_average_apartment_prices_by_city(city)


# 8. Grupowanie statystyk mieszkań na sprzedaż od poszczególnych firm
@sales_router.get("/companies/sale-offers/statistics")
def get_companies_sales_statistics(company_name: t.Optional[str] = '') -> t.List[CompanyStatisticResult]:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.get_companies_sales_statistics(company_name)


# 9. Wyszkiwanie mieszkania po id
@sales_router.get("/apartments/{apartment_id}")
def search_apartments(apartment_id: str) -> ApartmentInfo:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.find_apartment_by_id(apartment_id)


# 10. Zwrócenie informacji o firmach i mieszkaniach oferowanych przez nie
@sales_router.get("/owners/{owner_id}")
def get_owner_by_id(owner_id: str) -> OwnerApiModel:
    reader_manager: ReaderManager = READER_MANAGER
    return reader_manager.get_owner_by_id(owner_id)
