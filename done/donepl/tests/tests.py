from django.test import Client
# Create your tests here.


def test_main():
    client = Client()
    response = client.get('/main/')
    assert response.status_code == 200
