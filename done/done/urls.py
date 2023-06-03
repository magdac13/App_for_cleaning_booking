"""done URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from donepl.views import MainView, MapView, AboutView, RegisterView, ServiceView, CreateOrderView, LiveWorkerView, \
    PaymentView, RegisterCustomerView, RegisterWorkerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', MainView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('map/', MapView.as_view(), name='map'),
    path('about/', AboutView.as_view(), name='about'),
    path('live_location/', LiveWorkerView.as_view(), name='live_location'),
    path('service/', ServiceView.as_view(), name='service'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('register_customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('register_worker/', RegisterWorkerView.as_view(), name='register_worker'),





]
