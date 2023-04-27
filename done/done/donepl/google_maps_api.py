import googlemaps
from geopy.geocoders import GoogleV3
from done.done import settings
from done.done.donepl.models import User

geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
location = geolocator.geocode
class GoogleMapsApi:

    users = User.objects.all()

    def __new__(cls, **api_key):
        if api_key:
            cls.api_key = api_key
        if (
            hasattr(settings, 'GOOGLE_MAPS_API_KEY')
            and settings.GOOGLE_MAPS_API_KEY != ''
        ):
            cls.api_key = settings.GOOGLE_MAPS_API_KEY
            cls.gmaps = googlemaps.Client(key=cls.api_key)
            return super(GoogleMapsApi, cls).__new__(cls)

    def geolocate(self, users, home_mobile_country_code=None,
                  home_mobile_network_code=None, radio_type=None, carrier=None,
                  consider_ip=None, cell_towers=None, wifi_access_points=None):
