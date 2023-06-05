from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotAllowed, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import FormView, CreateView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import LoginForm, ServiceForm, OrderForm, RegisterForm, RegisterCustomerForm, RegisterWorkerForm
from .models import Worker, Customer, Service, Order
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')
    

class StartView(View):
    def get(self, request):
        return redirect('main')


class PricingView(View):
    def get(self, request):
        return render(request, 'pricing.html')


class MapView(View):
    """ """

    def get_nearby_workers(self, request, services=[]):
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
            distance__lte=Distance(m=10000000000),  # adjust the distance threshold as needed
            # services
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

            service_names = form.cleaned_data['name']
            service = Service.objects.filter(name__in=service_names).first()
            print(service)

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
            names = form.cleaned_data['name']
            for name in names:
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
    # form_class = RegisterForm
    # template_name = 'register.html'
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            User.objects.create_user(
                   username=form.cleaned_data['username'],
                   password=form.cleaned_data['password'],
                   first_name=form.cleaned_data['first_name'],
                   last_name=form.cleaned_data['last_name'],
                   email=form.cleaned_data['email']
                           )
            return redirect('map')
        print('niepoprawwny formularz')
        return render(request, 'live_location.html', context={'form': form})

    # def define_user_type(self, form):
#
    #     user_type = form.cleaned_data['user_type']
#
    #     if user_type == 'customer':
    #         return redirect('register_customer')
    #     else:
    #         return redirect('register_worker')

    # def form_valid(self, form):
    #     form = RegisterForm(request.POST)
    #     if User.objects.filter(username=form.cleaned_data['username']).exists():
    #         form.add_error('username', "User already exists")
    #         return super().form_invalid(form)
#
    #     if form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
    #         form.add_error('repeat_password', "Passwords do not match")
    #         return super().form_invalid(form)
#
    #     User.objects.create_user(
    #         username=form.cleaned_data['username'],
    #         password=form.cleaned_data['password'],
    #         first_name=form.cleaned_data['first_name'],
    #         last_name=form.cleaned_data['last_name'],
    #         email=form.cleaned_data['email']
#
    #     )
    #     return super().form_valid(form)


class RegisterCustomerView(View):
    def get(self, request):
        form = RegisterCustomerForm()
        return render(request, 'customer_registration.html', context={'form': form})


class RegisterWorkerView(View):
    def get(self, request):
        form = RegisterWorkerForm()
        return render(request, 'worker_registration.html', context={'form': form})


class CreateOrderView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'live_location.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            order = Order(
                worker=form.cleaned_data['worker'],
                service=form.cleaned_data['service'],
                customer=request.user.customer,
                date_time=timezone.now()

            )

            order.save()
            return redirect('payment')
        return render(request, 'payment.html', {'form': form})


class PaymentView(View):
    def get(self, request):
        return render(request, 'payment.html')

    def post(self, request):
        return render(request, 'payment.html')
