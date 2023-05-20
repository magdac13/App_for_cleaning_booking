from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Worker, Customer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class MapView(View):
    def get(self, request):

        context = {
            'google_api_key': settings.GOOGLE_MAPS_API_KEY
        }
        return render(request, 'live_location.html', context)


class LiveLocationView(View):
    def get(self, request, *args, **kwargs):

        customer_location_data = {
            'longitude': float(request.GET['lng']),
            'latitude': float(request.GET['lat'])
        }

        # customer = Customer.objects.create(
            #customer_location=Point(customer_location_data['longitude'], customer_location_data['latitude'])
        #)
        # Calculate distance between worker and nearby customers
        nearby_customers = Worker.objects.annotate(
            distance=DistanceFunc('worker_location', Point(customer_location_data['longitude'], customer_location_data['latitude'], srid=4326))
        ).filter(
            distance__lte=Distance(m=1000000)  # adjust the distance threshold as needed
        ).order_by('distance')[:10]
        # Retrieve the coordinates of nearby customers
        nearby_customer_locations = [{'latitude': c.worker_location.y, 'longitude': c.worker_location.x} for c in
                                     nearby_customers]
        # Return the nearby customer locations as a JSON response
        return JsonResponse(nearby_customer_locations, safe=False)


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

