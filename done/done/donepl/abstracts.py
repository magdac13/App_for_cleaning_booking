from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
import requests

from done.done.donepl.models import Job


_GEOLOCATION_BASE_URL = "https://www.googleapis.com"


class UserAbs(User):

    jobs = models.ManyToManyField(Job, related_name="user_jobs")

    def get_jobs(self):
        return ", ".join([str(p) for p in self.jobs.all()])

    def set_job(self, job):
        self.jobs.set(job)

    def remove_job(self, job):
        self.jobs.remove(job)

    def clear_prace(self):
        self.jobs.clear()


class GeoUserAbs(User):

    """
    Geodata fields for the User class
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.user_longitude = self.user_longitude

    def get_location_from_user_address(self):
        user = User.objects.get(pk=User.pk)
        user_live_address = user.user_address

        user_live_address.geom = {'type': 'Point', 'coordinates': [self.user_longitude, user_latitude]}

    
    # Address data 
    address_street = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=100, blank=True, null=True)
    address_zipcode = models.CharField(max_length=100, blank=True, null=True)
    
    def update_google_data(self):
        
        """
        Updates Google API data. Requires google api authentication key.
        :return:
        """
        user = User.objects.get(pk=User.pk)
        user_live_address = user.user_address
        user_longitude = user_live_address.geom.get('coordinates')[0]
        user_latitude = user_live_address.geom.get('coordinates')[0]

        url = f'https://maps.googleapis.com/maps/api/geocode/json?' \
            f'latlng= {user_latitude},{user_longitude}&key={settings.GOOGLE_MAPS_API}' \
            f'&key={settings.GOOGLE_MAPS_API_KEY}'

        request = requests.get(url)
        if request.status_code == 200:
            self.google_api_data = request.json()
            self.save()

    def show_user_location(request):
        # Pobierz aktualne współrzędne geograficzne użytkownika

        user_latitude = request.POST.get('latitude')
        user_longitude = request.POST.get('longitude')
        # Przekaż klucz API dla Google Maps

        api_key = settings.GOOGLE_MAPS_API_KEY

        # Zbuduj url zapytania do Google Maps
        url = f'https://maps.googleapis.com/maps/api/js?key={api_key}'

        # Przekaż współrzędne użytkownika do szablonu HTML
        context = {'latitude': user_latitude, 'longitude': user_longitude, 'api_url': url}

        # Zwróć szablon HTML z zaimplementowaną mapą
        return render(request, 'main.html', context)


class JobAbs(Job):

    # Obliczenie ceny na podstawie czasu oraz odległości za
    # pomocą Google Maps Distance Matrix API

    def price(self):

        user_address = User.objects.filter(user=self)
        origin = settings.MY_APP_ADDRESS
        destination = user_address.address

        # Tworzenie zapytania do API Google Maps
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"
        url += "&origins=" + origin.replace(' ', '+')
        url += "&destinations=" + destination.replace(' ', '+')
        url += "&key=" + settings.GOOGLE_MAPS_API_KEY

        # Wysyłanie zapytania i otrzymanie odpowiedzi w formacie JSON
        response = requests.get(url)
        data = response.json()

        # Pobranie czasu oraz odległości z odpowiedzi API
        duration_text = data['rows'][0]['elements'][0]['duration']['text']
        distance_text = data['rows'][0]['elements'][0]['distance']['text']

        # Obliczenie ceny na podstawie czasu oraz odległości
        price = 10 * float(duration_text.split()[0]) + 5 * float(distance_text.split()[0])

        if self.name == 'House cleaning':
            price *= 1.2

        elif self.name == 'Handy Man':
            price *= 1.05

        elif self.name == 'Car cleaning':
            price *= 1.1

        elif self.name == 'Kitchen cleaning':
            price *= 1.05

        elif self.name == 'Bath cleaning':
            price *= 1.2

        elif self.name == 'Window cleaning':
            price *= 1.1

        elif self.name == 'Garage cleaning':
            price *= 1.2

        elif self.name == 'Cooking':
            price *= 1.05

        elif self.name == 'Clothes Washing':
            price *= 1.05

        elif self.name == 'Dog walking':
            price *= 1.00

        elif self.name == 'Pet feeding':
            price *= 1.03

        elif self.name == 'Dishwashing':
            price *= 1.05

        elif self.name == 'Lawn mowing':
            price *= 1.1

        elif self.name == 'Plants watering':
            price *= 1.03

        return price
