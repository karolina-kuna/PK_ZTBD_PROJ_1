class Offer:
    def __init__(self, address_city: str,
                 address_street: str,
                 offer_id: str,
                 title: str,
                 price: float,
                 area: float,
                 status: str,
                 owner_id: str,
                 apartment_id: str,
                 company_name: str):
        self.address_city = address_city
        self.address_street = address_street
        self.offer_id = offer_id
        self.title = title
        self.price = price
        self.area = area
        self.status = status
        self.owner_id = owner_id
        self.apartment_id = apartment_id
        self.company_name = company_name


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
        self.owner_id = owner_id
        self.address_id = address_id


class Owner:
    def __init__(self, owner_id: str, name: str, surname: str, phone_number: str, address: str, email_address: str,
                 company_name: str):
        self.owner_id = owner_id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.address = address
        self.email_address = email_address
        self.company_name = company_name


class Address:
    def __init__(self, address_id:str, city: str, street_name: str, building_nr: str, apartment_nr: str, postal_code: str):
        self.address_id = address_id
        self.city = city
        self.street_name = street_name
        self.building_nr = building_nr
        self.apartment_nr = apartment_nr
        self.postal_code = postal_code
