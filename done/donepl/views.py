from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import FormView, CreateView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import LoginForm, ServiceForm, OrderForm
from .models import Worker, Customer, Service, Order
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class MapView(View):

    def get_nearby_workers(self, request):
        customer_location_data = {
            'longitude': float(request.GET.get('lng', 21.134200062347926)),
            'latitude': float(request.GET.get('lat', 52.27965560005034))
        }

        # customer = Customer.objects.create(
            #customer_location=Point(customer_location_data['longitude'], customer_location_data['latitude'])
        #)

        # Calculate distance between customer and nearby workers
        nearby_workers = Worker.objects.annotate(
            distance=DistanceFunc('worker_location', Point(customer_location_data['longitude'], customer_location_data['latitude'], srid=4326))
        ).filter(
            distance__lte=Distance(m=10000000000)  # adjust the distance threshold as needed
        ).order_by('distance')[:10]
        # Retrieve the coordinates of nearby workers
        # nearby_worker_locations = [{'latitude': c.worker_location.y, 'longitude': c.worker_location.x} for c in
        # nearby_workers]
        # Return the nearby customer locations as a JSON response
        return nearby_workers

    def get(self, request):
        nearby_workers = self.get_nearby_workers(request)
        context = {
            'google_api_key': settings.GOOGLE_MAPS_API_KEY,
            'nearby_workers': nearby_workers
        }

        return render(request, 'live_location.html', context)

    def post(self, request):
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['name']
            nearby_workers = self.get_nearby_workers(request)
            context = {
                'google_api_key': settings.GOOGLE_MAPS_API_KEY,
                'service': service,
                'nearby_workers': nearby_workers
            }
            return render(request, 'live_location.html', context)
        return render(request, 'service.html', {'form': form})


class LiveWorkerView(MapView):

    def get(self, request, *args, **kwargs):
        nearby_workers = self.get_nearby_workers(request)
        nearby_worker_locations = [{'latitude': c.worker_location.y, 'longitude': c.worker_location.x} for c in
                                   nearby_workers]

        return JsonResponse(nearby_worker_locations, safe=False)


class ServiceView(FormView):

    def get(self, request):
        form = ServiceForm()
        return render(request, 'service.html', context={'form': form})

    def post(self, request):
        form = ServiceForm(request.POST)
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data['name']
            service = Service()
            service.name = name
            service.save()

            return redirect('map')
        print('niepoprawwny formularz')
        return render(request, 'live_location.html', context={'form': form})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class CreateOrderView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'live_location.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                worker_id=form.cleaned_data['worker_id'],
                service=form.cleaned_data['service'],
                location=form.cleaned_data['location'],
                hours=form.cleaned_data['hours'],
                customer=request.user.customer
            )
            order.save()
            return redirect('payment')  # Przekieruj na stronę płatności
        return render(request, 'payment.html', {'form': form})



