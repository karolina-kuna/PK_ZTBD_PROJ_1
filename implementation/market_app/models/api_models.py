from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from market_app.models.db_models.cassandra_models import Apartment, Offer


class ApartmentForSaleSearchQuery(BaseModel):
    city: str
    street_name: str


class SaleOffer(BaseModel):
    creation_date: datetime
    price: float
    is_negotiable: bool
    title: str
    status: str
    modification_date: Optional[datetime]
    description: Optional[str]
    agency_fee: Optional[float]


class Address(BaseModel):
    address_id: Optional[str]
    street_name: str
    building_nr: str
    apartment_nr: str
    postal_code: str
    city: str


class OwnerApiModel(BaseModel):
    owner_id: Optional[str]
    name: str
    surname: str
    phone_number: str
    address: str
    email_address: str
    company_name: Optional[str]


class ApartmentInfo(BaseModel):
    apartment_id: str
    area: float
    creation_year: int
    last_renovation_year: Optional[int]
    building_type: str
    heating_type: str
    furnished: bool
    rooms_count: int
    address_id: str
    address: Optional[Address]
    owner_id: str
    owner: Optional[OwnerApiModel]


class ApartmentOfferSearchResult(BaseModel):
    offer_id: str
    apartment_id: str
    city: str
    street: str
    price: float
    is_negotiable: bool
    title: str
    status: str


class ApartmentPriceRangeQuery(BaseModel):
    city: str
    min_price: float
    max_price: float


class ApartmentPriceRange(BaseModel):
    min_price: float
    max_price: float


class ApartmentUpdateInfo(BaseModel):
    area: Optional[float]
    creation_year: Optional[int]
    last_renovation_year: Optional[int]
    building_type: Optional[str]
    heating_type: Optional[str]
    furnished: Optional[bool]
    rooms_count: Optional[int]
    address_id: Optional[str]
    owner_id: Optional[str]


class SaleOfferStatusUpdate(BaseModel):
    status: str


class ApartmentPriceByDistrict(BaseModel):
    district: str
    average_price: float


class ApartmentSaleOffersByStatusQuery(BaseModel):
    company_name: Optional[str]
    status: Optional[str]


class ApartmentSaleOffersByStatus(BaseModel):
    company_name: str
    apartments: List[ApartmentInfo]
    status: str


class ApartmentSearchQuery(BaseModel):
    address: Optional[str]
    price: Optional[float]


class ApartmentOfferAveragePrice(BaseModel):
    city: str
    avg_price: float
    avg_price_per_m2: float


class CompanyStatisticResult(BaseModel):
    company_name: str
    avg_price: float
    avg_price_per_m2: float
    sales_offer_count: int


class CompanyAndApartments(BaseModel):
    company_name: str
    apartments: List[ApartmentInfo]


class FullApartment(BaseModel):
    apartment: ApartmentInfo
    owner: OwnerApiModel
    offers: List[SaleOffer]
    address: Address


class FullApartmentResponse:
    def __init__(self, apartment: Apartment, owner: OwnerApiModel, offers: List[Offer], address: Address):
        self.apartment = apartment
        self.owner = owner
        self.offers = offers
        self.address = address
