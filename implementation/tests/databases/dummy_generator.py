import json
import random
import string
from datetime import datetime, timedelta

from market_app.models.api_models import ApartmentInfo, Address, OwnerApiModel, SaleOffer, FullApartment
from market_app.services.cassandra_service import CassandraService


def generate_random_apartment_info():
    return ApartmentInfo(
        apartment_id=str(random.randint(10000, 99999)),
        area=random.uniform(20, 200),
        creation_year=random.randint(1900, 2021),
        last_renovation_year=random.randint(1900, 2021),
        building_type=random.choice(['apartment building', 'single-family home', 'townhouse']),
        heating_type=random.choice(['central', 'electric', 'gas']),
        furnished=random.choice([True, False]),
        rooms_count=random.randint(1, 10),
        owner_id=2,
        address_id=2
    )


def generate_random_address():
    return Address(
        id="",
        street_name=random.choice(['Main St', 'High St', 'Broadway', 'Park Ave']),
        building_nr=str(random.randint(1, 200)),
        apartment_nr=str(random.randint(1, 200)),
        postal_code=random.choice(['12345', '54321', '98765', '67890']),
        city=random.choice(['New York', 'Chicago', 'Los Angeles', 'Houston'])
    )


def generate_random_owner():
    names = ['John', 'Michael', 'Jessica', 'Sara', 'George']
    surnames = ['Smith', 'Williams', 'Johnson', 'Brown', 'Jones']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
    streets = ['Main St', 'Second St', 'Park Ave', 'Broadway']
    email_providers = ['gmail.com', 'outlook.com', 'yahoo.com', 'aol.com']

    name = random.choice(names)
    surname = random.choice(surnames)
    phone_number = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    address = f"{random.choice(cities)} , ul. {random.choice(streets)}, {str(random.randint(1, 200))}/ {str(random.randint(1, 200))} {random.randint(10000, 99999)}"
    email_address = f"{name.lower()}.{surname.lower()}@{random.choice(email_providers)}"
    company_name = None if random.random() > 0.5 else f"{name}'s Company"

    return OwnerApiModel(
        id="",
        name=name,
        surname=surname,
        phone_number=phone_number,
        address=address,
        email_address=email_address,
        company_name=company_name
    )


def generate_random_sale_offer():
    creation_date = datetime.now()
    price = random.uniform(100, 100000)
    is_negotiable = bool(random.getrandbits(1))
    title = random.choice(["Sprzedam mieszkanie", "Wynajmę mieszkanie", "Mam do wynajęcia pokój"])
    status = random.choice(["aktywny", "zakończony", "archiwalny"])
    modification_date = random.choice([datetime.now(), None])
    description = "".join(random.choices(string.ascii_letters + string.digits, k=200))
    agency_fee = random.uniform(0, price)
    return SaleOffer(creation_date=creation_date, price=price, is_negotiable=is_negotiable, title=title,
                     status=status, modification_date=modification_date, description=description,
                     agency_fee=agency_fee)


def generate_random_full_apartment(sales_size):
    apartment_info = generate_random_apartment_info()
    owner = generate_random_owner()
    offers = [generate_random_sale_offer() for _ in range(sales_size)]
    address = generate_random_address()
    return FullApartment(apartment=apartment_info, owner=owner, offers=offers, address=address)
