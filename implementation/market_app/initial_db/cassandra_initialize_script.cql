CREATE TABLE market_app.apartment
(
    apartment_id         uuid PRIMARY KEY,
    area                 float,
    creation_year        int,
    last_renovation_year int,
    building_type        text,
    heating_type         text,
    is_furnished         boolean,
    rooms_count          int,
    owner_id             text,
    address_id           text
);

CREATE TABLE market_app.owner
(
    owner_id      uuid PRIMARY KEY,
    name          text,
    surname       text,
    phone_number  text,
    address       text,
    email_address text,
    company_name  text
);

CREATE TABLE market_app.offers_by_city_and_street
(
    address_city   text,
    address_street text,
    offer_id       uuid,
    status         text,
    title          text,
    price          float,
    area           float,
    owner_id       text,
    apartment_id   text,
    PRIMARY KEY (address_city, address_street, offer_id)
);

CREATE TABLE market_app.offers_by_city_and_price
(
    address_city   text,
    address_street text,
    price          float,
    status         text,
    offer_id       uuid,
    title          text,
    area           float,
    owner_id       text,
    apartment_id   text,
    PRIMARY KEY ((address_city), price, offer_id)
);

CREATE TABLE market_app.offers_by_company_name
(
    company_name text,
    offer_id     uuid,
    title        text,
    status       text,
    area         float,
    price        float,
    owner_id     text,
    apartment_id text,
    PRIMARY KEY (company_name, offer_id)
);

CREATE TABLE IF NOT EXISTS market_app.address
(
    address_id   uuid PRIMARY KEY,
    city         text,
    street_name  text,
    building_nr  text,
    apartment_nr text,
    postal_code  text
);

CREATE TABLE market_app.offers_basic
(
    offer_id       uuid,
    address_city   text,
    address_street text,
    company_name   text,
    price          float,
    PRIMARY KEY (offer_id)
);

-- Wymagana zmiana w konfiguracji - https://stackoverflow.com/questions/9905795/is-there-any-query-for-cassandra-as-same-as-sqllike-condition

CREATE CUSTOM INDEX idx_address_street ON market_app.offers_by_city_and_street (address_street)
    USING 'org.apache.cassandra.index.sasi.SASIIndex'
    WITH OPTIONS = {
        'mode': 'CONTAINS',
        'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.NonTokenizingAnalyzer',
        'case_sensitive': 'false'};