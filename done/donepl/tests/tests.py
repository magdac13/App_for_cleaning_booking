from django.contrib.auth.models import User
from django.test import Client
# Create your tests here.
from django.test import TestCase, RequestFactory
from django.urls import reverse

from django.urls import reverse
from django.contrib.gis.geos import Point
from donepl.views import MapView, ServiceView, CreateOrderView, LiveWorkerView
from donepl.forms import ServiceForm, OrderForm
from donepl.models import Order, Worker, Service


class MapViewTest(TestCase):

    def test_get_request(self):
        response = self.client.get(reverse('map-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live_location.html')

    def test_post_request_with_invalid_form(self):
        data = {
            'name': '',  # puste pole, nie spełnia wymagań formularza
            # inne wymagane pola formularza
        }
        response = self.client.post(reverse('map-view'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service.html')

    def test_post_request_with_valid_form(self):
        data = {
            'name': 'Some Service',
            # inne wymagane pola formularza
        }
        response = self.client.post(reverse('map-view'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live_location.html')

    def test_main():
        client = Client()
        response = client.get('/main/')
        assert response.status_code == 200

    def test_get_nearby_workers(self):
        request = self.client.get(reverse('map-view'))
        view = MapView()
        nearby_workers = view.get_nearby_workers(request)
        self.assertEqual(len(nearby_workers), 10)  # sprawdź, czy zwracana lista ma oczekiwany rozmiar
        # inne asercje, w zależności od oczekiwanego formatu wyniku


class LiveWorkerViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Utwórz testowych pracowników
        Worker.objects.create(worker_location=Point(21.134200062347926, 52.27965560005034))
        Worker.objects.create(worker_location=Point(21.134200062347926, 52.27965560005034))
        Worker.objects.create(worker_location=Point(21.134200062347926, 52.27965560005034))
        Worker.objects.create(worker_location=Point(21.134200062347926, 52.27965560005034))
        Worker.objects.create(worker_location=Point(21.134200062347926, 52.27965560005034))

    def test_get_request(self):
        # Create request Factory
        factory = RequestFactory()

        # Create request factory
        request = factory.get(reverse('live-worker-view'))

        # Create view intance
        view = LiveWorkerView.as_view()

        # Realise request and get response
        response = view(request)

        # Check status code of response
        self.assertEqual(response.status_code, 200)

        # Check response format
        self.assertEqual(response['Content-Type'], 'application/json')

        # Check response data
        response_data = response.json()
        self.assertEqual(len(response_data), 5)  # Check if predicted number of workers is equal to 5
        # Add other assertions, depending on predicted format of the answer and context


class ServiceViewTest(TestCase):

    def test_get_request(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie GET
        request = factory.get(reverse('service-view'))

        # Utwórz instancję widoku
        view = ServiceView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź kod statusu odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy poprawny szablon został użyty
        self.assertTemplateUsed(response, 'service.html')

        # Sprawdź, czy formularz jest dostępny w kontekście odpowiedzi
        self.assertIsInstance(response.context_data['form'], ServiceForm)

    def test_post_request_with_valid_form(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie POST z poprawnymi danymi
        data = {'name': 'Test Service'}
        request = factory.post(reverse('service-view'), data)

        # Utwórz instancję widoku
        view = ServiceView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź, czy przekierowanie zostało wykonane na właściwy URL
        self.assertRedirects(response, reverse('map'))

        # Sprawdź, czy nowa usługa została utworzona w bazie danych
        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.first()
        self.assertEqual(service.name, 'Test Service')

    def test_post_request_with_invalid_form(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie POST z niepoprawnymi danymi
        data = {'name': ''}
        request = factory.post(reverse('service-view'), data)

        # Utwórz instancję widoku
        view = ServiceView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź kod statusu odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy poprawny szablon został użyty
        self.assertTemplateUsed(response, 'live_location.html')

        # Sprawdź, czy formularz jest dostępny w kontekście odpowiedzi
        self.assertIsInstance(response.context_data['form'], ServiceForm)

        # Sprawdź, czy formularz zawiera błędy
        self.assertTrue(response.context_data['form'].errors)


class CreateOrderViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Utwórz użytkownika do testów
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user.save()

    def test_get_request(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie GET
        request = factory.get(reverse('create-order-view'))

        # Utwórz instancję widoku
        view = CreateOrderView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź kod statusu odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy poprawny szablon został użyty
        self.assertTemplateUsed(response, 'live_location.html')

        # Sprawdź, czy formularz jest dostępny w kontekście odpowiedzi
        self.assertIsInstance(response.context_data['form'], OrderForm)

    def test_post_request_with_valid_form(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie POST z poprawnymi danymi
        data = {
            'worker_id': 1,
            'service': 'Some Service',
            'location': 'Some Location',
            'hours': 2,
        }
        request = factory.post(reverse('create-order-view'), data)

        # Utwórz instancję widoku
        view = CreateOrderView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź, czy przekierowanie zostało wykonane na właściwy URL
        self.assertRedirects(response, reverse('payment'))

        # Sprawdź, czy nowe zamówienie zostało utworzone w bazie danych
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.worker_id, 1)
        self.assertEqual(order.service, 'Some Service')
        self.assertEqual(order.location, 'Some Location')
        self.assertEqual(order.hours, 2)
        self.assertEqual(order.customer, request.user.customer)

    def test_post_request_with_invalid_form(self):
        # Utwórz fabrykę żądań
        factory = RequestFactory()

        # Utwórz żądanie POST z niepoprawnymi danymi
        data = {
            'worker_id': 1,
            'service': '',
            'location': 'Some Location',
            'hours': 2,
        }
        request = factory.post(reverse('create-order-view'), data)

        # Utwórz instancję widoku
        view = CreateOrderView.as_view()

        # Wykonaj żądanie i otrzymaj odpowiedź
        response = view(request)

        # Sprawdź kod statusu odpowiedzi
        self.assertEqual(response.status_code, 200)

        # Sprawdź, czy poprawny szablon został użyty
        self.assertTemplateUsed(response, 'payment.html')

        # Sprawdź, czy formularz jest dostępny w kontekście odpowiedzi
        self.assertIsInstance(response.context_data['form'], OrderForm)

        # Sprawdź, czy formularz zawiera błędy
        self.assertTrue(response.context_data['form'].errors)