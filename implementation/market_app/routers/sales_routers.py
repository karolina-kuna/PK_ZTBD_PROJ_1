import typing as t

from fastapi import APIRouter, HTTPException, status
from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentInfo, ApartmentForSaleSearchResult, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceByDistrict, ApartmentSaleOffersByStatusQuery, ApartmentSaleOffersByStatus, ApartmentSearchQuery, \
    ApartmentSearchResult, CompanyAndApartments

sales_router = APIRouter(prefix="/authors", tags=["Authors"])


# 1.	Wyszukiwanie mieszkania do kupna po mieście i adresie
# a.	Pobranie szczegółów dotyczących mieszkania
# b.	Pobranie szczegółów dotyczących właściciela
@sales_router.get("/apartments/for-sale/search")
def search_apartments_for_sale(query: ApartmentForSaleSearchQuery) -> t.List[ApartmentForSaleSearchResult]:
    pass


@sales_router.post("/apartments")
def add_apartment_info(apartment_id: int, apartment_info: ApartmentInfo) -> None:
    pass


# 3.	Wyświetlenie informacji o przedziale informacjach cenowych w danej lokalizacji
@sales_router.get("/apartments/for-sale/prices")
def get_apartment_price_range(query: ApartmentPriceRangeQuery) -> ApartmentPriceRange:
    pass


# 4. Usunięcie oferty sprzedaży mieszkania
@sales_router.delete("/apartments/sale-offers/{apartment_id}")
def delete_apartment_sale_offer(apartment_id: int) -> None:
    pass


# 5. Zmiana danych mieszkania
@sales_router.patch("/apartments/{apartment_id}")
def update_apartment(apartment_id: int, update_info: ApartmentUpdateInfo) -> None:
    pass


# 6. Zmiana statusu oferty kupna
@sales_router.patch("/apartments/sale-offers/{offer_id}/status")
def update_sale_offer_status(offer_id: int, update_info: SaleOfferStatusUpdate) -> SaleOffer:
    pass


# 7. Wyszukanie średnich cen mieszkań na metr kwadratowy po dzielnicy
def get_average_apartment_prices_by_city_and_street(city: str, street_name: str) -> ApartmentPriceByDistrict:
    pass


# 8. Grupowanie mieszkań na sprzedaż w zależności od statusu dla poszczególnych firm
@sales_router.get("/apartments/sale-offers/statuses")
def get_apartment_sale_offers_by_status(query: ApartmentSaleOffersByStatusQuery) -> t.List[ApartmentSaleOffersByStatus]:
    pass


# 9. Wyszkiwanie mieszkania do kupna po adresie i cenie
@sales_router.get("/apartments/search")
def search_apartments(query: ApartmentSearchQuery) -> t.List[ApartmentSearchResult]:
    pass


# 10. Zwrócenie informacji o firmach i mieszkaniach oferowanych przez nie
@sales_router.get("/companies/apartments")
def get_companies_and_apartments() -> t.List[CompanyAndApartments]:
    pass

