import requests
from django.core.management.base import BaseCommand
from rating.models import Brewery

class Command(BaseCommand):
    help = 'Populate breweries in the database'

    def handle(self, *args, **kwargs):
        # Clear existing breweries
        Brewery.objects.all().delete()

        # Fetch data from the Open Brewery DB API
        api_url = 'https://api.openbrewerydb.org/breweries'
        response = requests.get(api_url)
        data = response.json()

        # Populate the database with fetched data
        for brewery_data in data:
            Brewery.objects.create(
                id=brewery_data['id'],
                name=brewery_data['name'],
                phone=brewery_data['phone'],
                brewery_type=brewery_data['brewery_type'],
                address_1=brewery_data['address_1'],
                #city=brewery_data['city'],
                #state=brewery_data['state'],
                #description=brewery_data.get('description', '')
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated breweries'))
