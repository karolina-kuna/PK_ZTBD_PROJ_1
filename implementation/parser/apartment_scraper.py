import csv
import overpy


def generate_addresses_into_csv(bbox, city_name):
    # Zapytanie do Overpass API, które pobiera nazwy ulic, numery budynków i numery mieszkań w Krakowie
    query = f"""
    [out:json]
    [bbox: {bbox}];
    node["addr:housenumber"]["addr:postcode"];
    out body;
    """

    print(query)

    api = overpy.Overpass()
    result = api.query(query)
    print(f"Ilość wyników: {len(result.nodes)}")

    # Otwórz plik CSV do zapisu
    with open(f"adresses_{city_name}.csv", "w", newline="", encoding='utf-8') as csv_file:
        # Utwórz obiekt writer CSV
        writer = csv.DictWriter(csv_file,
                                fieldnames=["StreetName", "buldingNr", "apartmentNr", "postalCode", "city",
                                            "district"])

        # Zapisz nagłówki w pliku CSV
        writer.writeheader()

        print(f"Resultatów: {len(result.nodes)} dla miasta: {city_name}")

        # Przejdź przez wszystkie węzły zwracane przez zapytanie
        for node in result.nodes:
            # Pobierz dane o adresie z węzła
            street_name = node.tags.get("addr:street", "")
            building_nr = node.tags.get("addr:housenumber", "")
            apartment_nr = node.tags.get("addr:flats", "")
            postal_code = node.tags.get("addr:postcode", "")
            city = node.tags.get("addr:city", "")

            # Zapisz dane o adresie w pliku CSV
            writer.writerow({
                "StreetName": street_name,
                "buldingNr": building_nr,
                "apartmentNr": apartment_nr,
                "postalCode": postal_code,
                "city": city,
                "district": " "
            })


city_with_bbox = [
    ['Kraków', '50.013123,19.836365,50.109218,20.041672'],
    ['Łódź', '51.689372,19.193871,51.835565,19.715378'],
    ['Warszawa', '52.067689,20.475082,52.357151,21.518097'],
    ['Wrocław', '51.035565,16.788139,51.183862,17.309647'],
    ['Poznań', '52.336849,16.657127,52.480940,17.178635']
]

for single_city_with_bbox in city_with_bbox:
    generate_addresses_into_csv(single_city_with_bbox[1], single_city_with_bbox[0])
