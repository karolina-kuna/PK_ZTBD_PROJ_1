import requests
from bs4 import BeautifulSoup

url = 'https://kazo.pl/krakow_krakow?page=2'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

prices = soup.find_all('span', class_='estate_price')

print(prices)