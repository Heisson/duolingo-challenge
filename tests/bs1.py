from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://duome.eu/'

username = 'heiss.on'

source = requests.get(f'{BASE_URL}{username}').text

soup = BeautifulSoup(source, 'lxml')

print(soup)
