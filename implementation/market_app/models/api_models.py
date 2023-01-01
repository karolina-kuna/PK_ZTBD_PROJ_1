from datetime import datetime
from typing import Optional, List


class ApartmentForSaleSearchQuery:
    city: str
    address: str


class SaleOffer:
    creation_date: datetime
    price: float
    is_negotiable: bool
    status: str
    modification_date: Optional[datetime]
    description: Optional[str]
    agency_fee: Optional[float]


class Address:
    street_name: str
    building_nr: str
    apartment_nr: str
    postal_code: str
    city: str


class Owner:
    name: str
    surname: str
    phone_number: str
    address: Address
    email_address: str
    company_name: Optional[str]


class ApartmentInfo:
    area: float
    creation_year: int
    last_renovation_year: Optional[int]
    building_type: str
    heating_type: str
    furnished: bool
    rooms_count: int
    address: Address
    owner: Owner


class ApartmentForSaleSearchResult:
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


class ApartmentPriceRangeQuery:
    city: str
    min_price: Optional[float]
    max_price: Optional[float]


class ApartmentPriceRange:
    min_price: float
    max_price: float


class ApartmentUpdateInfo:
    area: Optional[float]
    creation_year: Optional[int]
    last_renovation_year: Optional[int]
    building_type: Optional[str]
    heating_type: Optional[str]
    furnished: Optional[bool]
    rooms_count: Optional[int]
    address: Optional[Address]


class SaleOfferStatusUpdate:
    status: str


class ApartmentPriceByDistrict:
    district: str
    average_price: float


class ApartmentSaleOffersByStatusQuery:
    company_name: Optional[str]
    status: Optional[str]


class ApartmentSaleOffersByStatus:
    company_name: str
    apartments: List[ApartmentInfo]
    status: str


class ApartmentSearchQuery:
    address: Optional[str]
    price: Optional[float]


class ApartmentSearchResult:
    address: str
    price: float


class CompanyAndApartments:
    company_name: str
    apartments: List[ApartmentInfo]
