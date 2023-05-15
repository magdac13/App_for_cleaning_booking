from django.shortcuts import render
from django.views import View

from done import settings


# Create your views here.
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class MapView(View):
    def get(self, request):
        ctx = {'google_api_key': settings.GOOGLE_MAPS_API_KEY}
        return render(request, 'live_location.html', ctx)
