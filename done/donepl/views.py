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

    def post(self, request, *args, **kwargs):
        data = request.json()
        worker_location_data = data.get('workerLocation')
        customer_location_data = data.get('customerLocation')
        # Save worker's location in the database
        worker = Worker.objects.create(
            worker_location=Point(worker_location_data['longitude'], worker_location_data['latitude'])
        )
        customer = Customer.objects.create(
            customer_location=Point(customer_location_data['longitude'], customer_location_data['latitude'])
        )
        # Calculate distance between worker and nearby customers
        nearby_customers = Customer.objects.annotate(
            distance=DistanceFunc('customerLocation', worker.location)
        ).filter(
            distance__lte=Distance(m=1000)  # adjust the distance threshold as needed
        ).order_by('distance')[:10]
        # Retrieve the coordinates of nearby customers
        nearby_customer_locations = [{'latitude': c.location.y, 'longitude': c.location.x} for c in
                                     nearby_customers]
        # Return the nearby customer locations as a JSON response
        return JsonResponse(nearby_customer_locations, safe=False)


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

