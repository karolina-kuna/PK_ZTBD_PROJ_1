from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ApartmentForSaleSearchQuery(BaseModel):
    city: str
    address: str


class SaleOffer(BaseModel):
    creation_date: datetime
    price: float
    is_negotiable: bool
    status: str
    modification_date: Optional[datetime]
    description: Optional[str]
    agency_fee: Optional[float]


class Address(BaseModel):
    street_name: str
    building_nr: str
    apartment_nr: str
    postal_code: str
    city: str


class Owner(BaseModel):
    name: str
    surname: str
    phone_number: str
    address: Address
    email_address: str
    company_name: Optional[str]


class ApartmentInfo(BaseModel):
    area: float
    creation_year: int
    last_renovation_year: Optional[int]
    building_type: str
    heating_type: str
    furnished: bool
    rooms_count: int
    address: Address
    owner: Owner


class ApartmentForSaleSearchResult(BaseModel):
    id: int
    area: float
    creation_year: int
    last_renovation_year: Optional[int]
    building_type: str
    heating_type: str
    furnished: bool
    rooms_count: int
    address: Address
    owner: Owner
    sale_offer: SaleOffer


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
    address: Optional[Address]


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


class ApartmentSearchResult(BaseModel):
    address: str
    price: float


class CompanyAndApartments(BaseModel):
    company_name: str
    apartments: List[ApartmentInfo]
