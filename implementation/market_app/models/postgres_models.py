from datetime import date


class SaleOffer:
    def __init__(self,
                 offer_id: str,
                 price: float,
                 status: str,
                 negotiable: bool,
                 description: str,
                 agency_fee: float,
                 creation_date: date,
                 modification_date: date,
                 apartment_id: str,
                 ):
        self.offer_id = offer_id
        self.price = price
        self.status = status
        self.negotiable = negotiable
        self.description = description
        self.agency_fee = agency_fee
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.apartment_id = apartment_id


class Apartment:
    def __init__(self, apartment_id: str, area: float, creation_year: int, last_renovation_year: int,
                 building_type: str, heating_type: str, is_furnished: bool, rooms_count: int,
                 owner_id: str,
                 address_id: str):
        self.apartment_id = apartment_id
        self.area = area
        self.creation_year = creation_year
        self.last_renovation_year = last_renovation_year
        self.building_type = building_type
        self.heating_type = heating_type
        self.is_furnished = is_furnished
        self.rooms_count = rooms_count
        self.address_id = address_id
        self.owner_id = owner_id


class Owner:
    def __init__(self, owner_id: str, name: str, surname: str, phone_number: str,email_address: str,
                 company_name: str, address_id: int):
        self.owner_id = owner_id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.email_address = email_address
        self.company_name = company_name
        self.address_id = address_id


class Address:
    def __init__(self, address_id: str, city: str, street_name: str, building_nr: str, apartment_nr: str,
                 postal_code: str):
        self.address_id = address_id
        self.city = city
        self.street_name = street_name
        self.building_nr = building_nr
        self.apartment_nr = apartment_nr
        self.postal_code = postal_code
