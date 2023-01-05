import typing as t

from fastapi import APIRouter, HTTPException, status, Depends

from market_app.dependencies import get_reader_manager
from market_app.models.api_models import ApartmentForSaleSearchQuery, ApartmentInfo, ApartmentForSaleSearchResult, \
    ApartmentPriceRangeQuery, ApartmentPriceRange, SaleOfferStatusUpdate, SaleOffer, ApartmentUpdateInfo, \
    ApartmentPriceByDistrict, ApartmentSaleOffersByStatusQuery, ApartmentSaleOffersByStatus, ApartmentSearchQuery, \
    ApartmentSearchResult, CompanyAndApartments
from market_app.services.reader_manager import ReaderManager

sales_router = APIRouter(prefix="/authors", tags=["Authors"])


# 1.	Wyszukiwanie mieszkania do kupna po mieście i adresie
# a.	Pobranie szczegółów dotyczących mieszkania
# b.	Pobranie szczegółów dotyczących właściciela
@sales_router.get("/apartments/for-sale/search")
def search_apartments_for_sale(query: ApartmentForSaleSearchQuery,
                               reader_manager: ReaderManager = Depends(get_reader_manager)
                               ) -> t.List[ApartmentForSaleSearchResult]:
    return reader_manager.search_apartments_for_sale(query)


@sales_router.post("/apartments")
def add_apartment_info(apartment_id: int, apartment_info: ApartmentInfo,
                       reader_manager: ReaderManager = Depends(get_reader_manager)) -> None:
    reader_manager.add_apartment_info(apartment_info)


# 3.	Wyświetlenie informacji o przedziale informacjach cenowych w danej lokalizacji
@sales_router.get("/apartments/for-sale/prices")
def get_apartment_price_range(query: ApartmentPriceRangeQuery,
                              reader_manager: ReaderManager = Depends(get_reader_manager)) -> ApartmentPriceRange:
    return reader_manager.get_apartment_price_range(query)


# 4. Usunięcie oferty sprzedaży mieszkania
@sales_router.delete("/apartments/sale-offers/{offer_id}")
def delete_apartment_sale_offer(offer_id: int,
                                reader_manager: ReaderManager = Depends(get_reader_manager)) -> None:
    reader_manager.delete_apartment_sale_offer(offer_id)


# 5. Zmiana danych mieszkania
@sales_router.patch("/apartments/{apartment_id}")
def update_apartment(apartment_id: int, update_info: ApartmentUpdateInfo,
                     reader_manager: ReaderManager = Depends(get_reader_manager)) -> None:
    reader_manager.update_apartment(apartment_id, update_info)


# 6. Zmiana statusu oferty kupna
@sales_router.patch("/apartments/sale-offers/{offer_id}/status")
def update_sale_offer_status(offer_id: int, update_info: SaleOfferStatusUpdate,
                             reader_manager: ReaderManager = Depends(get_reader_manager)) -> SaleOffer:
    reader_manager.update_sale_offer_status(offer_id, update_info)


# 7. Wyszukanie średnich cen mieszkań na metr kwadratowy po dzielnicy
def get_average_apartment_prices_by_city_and_street(city: str, street_name: str,
                                                    reader_manager: ReaderManager = Depends(
                                                        get_reader_manager)) -> ApartmentPriceByDistrict:
    return reader_manager.get_average_apartment_prices_by_city_and_street(city, street_name)


# 8. Grupowanie mieszkań na sprzedaż w zależności od statusu dla poszczególnych firm
@sales_router.get("/apartments/sale-offers/statuses")
def get_apartment_sale_offers_by_status(query: ApartmentSaleOffersByStatusQuery,
                                        reader_manager: ReaderManager = Depends(
                                            get_reader_manager)) -> t.List[ApartmentSaleOffersByStatus]:
    return reader_manager.get_apartment_sale_offers_by_status(query)


# 9. Wyszkiwanie mieszkania do kupna po adresie i cenie
@sales_router.get("/apartments/search")
def search_apartments(query: ApartmentSearchQuery,
                      reader_manager: ReaderManager = Depends(
                          get_reader_manager)) -> t.List[ApartmentSearchResult]:
    return reader_manager.search_apartments(query)


# 10. Zwrócenie informacji o firmach i mieszkaniach oferowanych przez nie
@sales_router.get("/companies/apartments")
def get_companies_and_apartments(reader_manager: ReaderManager = Depends(
    get_reader_manager)) -> t.List[CompanyAndApartments]:
    return reader_manager.get_companies_and_apartments()
