import time
import concurrent.futures
import requests


def send_request():
    response = requests.get("http://localhost:8010/sales/apartments/sale-offers/by-price-range?city=New%20York&min_price=10000&max_price=65000")
    return response.status_code


def perform_test():
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_results = [executor.submit(send_request) for i in range(10)]
        for future in concurrent.futures.as_completed(future_results):
            pass

    end_time = time.time()

    total_time = end_time - start_time
    print(f'Total time: {total_time} seconds')


if __name__ == "__main__":
    perform_test()
