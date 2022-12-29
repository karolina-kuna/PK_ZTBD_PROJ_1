import csv
import random
import string

# Constants for data generation
MIN_YEAR = 1950
MAX_YEAR = 2020
MIN_PRICE = 10000
MAX_PRICE = 1000000
BUILDING_TYPES = ['brick', 'panel', 'block', 'monolithic']
HEATING_TYPES = ['central', 'individual', 'none']
CITIES = ['Warsaw', 'Krakow', 'Wroclaw', 'Poznan', 'Gdansk']

# Generate random data for the apartment table
apartments = []
for i in range(3000000):
  apartment = {}
  apartment['area'] = random.uniform(20, 150)
  apartment['creation_year'] = random.randint(MIN_YEAR, MAX_YEAR)
  apartment['last_renovation_year'] = random.randint(MIN_YEAR, MAX_YEAR)
  apartment['building_type'] = random.choice(BUILDING_TYPES)
  apartment['heating_type'] = random.choice(HEATING_TYPES)
  apartment['furnished'] = random.choice([True, False])
  apartment['rooms_count'] = random.randint(1, 5)
  apartments.append(apartment)

# Generate random data for the owner table
owners = []
for i in range(3000000):
  owner = {}
  owner['name'] = ''.join(random.choices(string.ascii_letters, k=10))
  owner['surname'] = ''.join(random.choices(string.ascii_letters, k=15))
  owner['phone_number'] = ''.join(random.choices(string.digits, k=9))
  owner['address'] = ''.join(random.choices(string.ascii_letters, k=20))
  owner['email_address'] = ''.join(random.choices(string.ascii_letters, k=10)) + '@example.com'
  owner['company_name'] = ''.join(random.choices(string.ascii_letters, k=20))
  owners.append(owner)

# Generate random data for the address table
addresses = []
for i in range(3000000):
  address = {}
  address['street_name'] = ''.join(random.choices(string.ascii_letters, k=15))
  address['building_nr'] = random.randint(1, 50)
  address['apartment_nr'] = random.randint(1, 100)
  address['postal_code'] = ''.join(random.choices(string.digits, k=6))
  address['city'] = random.choice(CITIES)
  addresses.append(address)

STATUSES = ['active', 'inactive']

# Generate random data for the sale offer table
offers = []
for i in range(3000000):
  offer = {}
  offer['creation_date'] = '2022-01-01'
  offer['price'] = random.uniform(MIN_PRICE, MAX_PRICE)
  offer['is_negotiable'] = random.choice([True, False])
  offer['status'] = random.choice(STATUSES)
  offer['modification_date'] = '2022-01-01'
  offer['description'] = ''.join(random.choices(string.ascii_letters, k=100))
  offer['agency_fee'] = random.uniform(0, 0.1)
  offers.append(offer)

# Write the offers data to a CSV file
with open('offers.csv', 'w', newline='') as csvfile:
  fieldnames = ['creation_date', 'price', 'is_negotiable', 'status', 'modification_date', 'description', 'agency_fee']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  writer.writeheader()
  for offer in offers:
    writer.writerow(offer)

# Write the apartments data to a CSV file
with open('apartments.csv', 'w', newline='') as csvfile:
  fieldnames = ['area', 'creation_year', 'last_renovation_year', 'building_type', 'heating_type', 'furnished', 'rooms_count']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  writer.writeheader()
  for apartment in apartments:
    writer.writerow(apartment)


# Write the owners data to a CSV file
with open('owners.csv', 'w', newline='') as csvfile:
  fieldnames = ['name', 'surname', 'phone_number', 'address', 'email_address', 'company_name']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  writer.writeheader()
  for owner in owners:
    writer.writerow(owner)