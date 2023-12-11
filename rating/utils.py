# utils.py

import requests
from .models import Brewery

def fetch_brewery_data():
    api_url = 'https://api.openbrewerydb.org/v1/breweries'
    response = requests.get(api_url)
    data = response.json()
    return data

def populate_breweries():
    brewery_data = fetch_brewery_data()
    for brewery in brewery_data:
        Brewery.objects.create(  # Ensure this is unique
            name=brewery['name'],
            phone=brewery['phone'],
            brewery_type=brewery['brewery_type'],
            address_1=brewery['address_1'],
            # Add other fields from the API as needed
        )
