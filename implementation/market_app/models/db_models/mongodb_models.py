class Owner:
    def __init__(self, surname: str, phone_number: str, address: str, email_address: str,
                 company_name: str, _id=None):
        if _id is not None:
            self._id = _id

        self.surname = surname
        self.phone_number = phone_number
        self.address = address
        self.email_address = email_address
        self.company_name = company_name

    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None


class Apartment:
    def __init__(self, area: float, creation_year: int, last_renovation_year: int, building_type: str,
                 heating_type: str, is_furnished: bool, rooms_count: int, _id=None):
        if _id is not None:
            self._id = _id
        self.area = area
        self.creation_year = creation_year
        self.last_renovation_year = last_renovation_year
        self.building_type = building_type
        self.heating_type = heating_type
        self.is_furnished = is_furnished
        self.rooms_count = rooms_count

    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None


class OfferAddress:
    def __init__(self, city: str, street: str, _id=None):
        if _id is not None:
            self._id = _id

        self.city = city
        self.street = street

    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None


class OfferOwner:
    def __init__(self, company_name: str, _id=None):
        if _id is not None:
            self._id = _id

        self.company_name = company_name
    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None



class Offer:
    def __init__(self, address: OfferAddress, price: int, title: str, area: int, owner: OfferOwner,
                 apartment_id: str, company_name: str, _id=None):
        if _id is not None:
            self._id = _id

        self.address = address
        self.price = price
        self.title = title
        self.area = area
        self.apartment_id = apartment_id
        self.company_name = company_name

    @property
    def id(self):
        return self._id if hasattr(self, '_id') else None
