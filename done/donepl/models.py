import random
from django.contrib.auth.models import User, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from geopy.distance import geodesic


# Create your models here.

class Service(models.Model):
    NAME_HOUSE_CLEANING = 'House cleaning'
    NAME_HANDY_MAN = 'Handy Man'
    NAME_CAR_CLEANING = 'Car cleaning'
    NAME_KITCHEN_CLEANING = 'Kitchen cleaning'
    NAME_BATH_CLEANING = 'Bath cleaning'
    NAME_WINDOW_CLEANING = 'Window cleaning'
    NAME_GARAGE_CLEANING = 'Garage cleaning'
    NAME_COOKING = 'Cooking'
    NAME_CLOTHES_WASHING = 'Clothes Washing'
    NAME_DOG_WALKING = 'Dog walking'
    NAME_PET_FEEDING = 'Pet feeding'
    NAME_DISHWASHING = 'Dishwashing'
    NAME_LAWN_MOWING = 'Lawn mowing'
    NAME_PLANTS_WATERING = 'Plants watering'

    JOBS_CHOICES = [
        (NAME_HOUSE_CLEANING, 'You can choose which rooms you want to clean as well as scope of cleaning'),
        (NAME_HANDY_MAN, 'Maintenance requests'),
        (NAME_CAR_CLEANING, 'Car cleaning services, available at gas station points or by your house'),
        (NAME_KITCHEN_CLEANING, 'Kitchen cleaning services'),
        (NAME_BATH_CLEANING, 'Bath cleaning services'),
        (NAME_WINDOW_CLEANING, 'Window cleaning services'),
        (NAME_GARAGE_CLEANING, 'Garage cleaning services'),
        (NAME_COOKING, 'Share your meals with neighbors'),
        (NAME_CLOTHES_WASHING, 'Clothes washing services'),
        (NAME_DOG_WALKING, 'Get your dog a walking buddy'),
        (NAME_PET_FEEDING, 'Feed your pets while not at home'),
        (NAME_DISHWASHING, 'Never get tired of dishwashing again'),
        (NAME_LAWN_MOWING, 'Ask your neighbor to mow your lawn'),
        (NAME_PLANTS_WATERING, "Don't let your plants dry out"),
    ]
    name = models.CharField(
        max_length=100, choices=JOBS_CHOICES
    )
    cost = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    order_time = models.DateTimeField(
        auto_now_add=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class Worker(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    date_of_birth = models.DateField()

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    gender = models.CharField(
        max_length=100
    )
    home_address = models.CharField(
        max_length=2, choices=GENDER_CHOICES
    )
    phone_number = models.CharField(
        max_length=100
    )

    rating = models.FloatField(
        default=5.0, validators=[
            MinValueValidator(3.0), MaxValueValidator(5.0)
        ]
    )
    worker_latitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    worker_longitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    services = models.ManyToManyField(
        Service, blank=True
    )

    photo = models.ImageField(
        upload_to='profile_photos', blank=True, null=True
    )

    def __str__(self):
        return self.user.first_name + '' + self.user.last_name

    def get_location(self):
        return self.worker_latitude, self.worker_longitude

    def set_location(self, worker_latitude, worker_longitude):
        self.worker_latitude = worker_latitude
        self.worker_longitude = worker_longitude
        self.save()

    def get_distance_to_customer(self, customer):
        worker_location = self.get_location()
        customer_location = customer.get_location()
        return geodesic(worker_location, customer_location).km


class Customer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    date_of_birth = models.DateField()

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    gender = models.CharField(
        max_length=100
    )
    home_address = models.CharField(
        max_length=2, choices=GENDER_CHOICES
    )
    phone_number = models.CharField(
        max_length=100
    )

    rating = models.FloatField(
        default=5.0, validators=[
            MinValueValidator(3.0), MaxValueValidator(5.0)
        ]
    )
    worker_latitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    worker_longitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    services = models.ManyToManyField(
        Service, blank=True
    )

    photo = models.ImageField(
        upload_to='profile_photos', blank=True, null=True
    )

    def __str__(self):
        return self.user.first_name + '' + self.user.last_name

    def get_location(self):
        return self.worker_latitude, self.worker_longitude

    def set_location(self, worker_latitude, worker_longitude):
        self.worker_latitude = worker_latitude
        self.worker_longitude = worker_longitude
        self.save()

    def get_distance_to_worker(self, worker):
        worker_location = self.get_location()
        customer_location = worker.get_location()
        return geodesic(worker_location, customer_location).km


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE
    )
    worker = models.ForeignKey(
        Worker, on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE
    )
    date_time = models.DateTimeField(
        default=timezone.now
    )
    location = models.CharField(
        max_length=255
    )
    hours = models.IntegerField()
    cost = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    worker_rating = models.DecimalField(
        max_digits=3, decimal_places=2
    )
    customer_rating = models.DecimalField(
        max_digits=3, decimal_places=2
    )

    def __str__(self):
        return f'{self.customer} - {self.service}'


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} paid {self.amount} on {self.timestamp}"

    def save(self, *args, **kwargs):
        self.amount = self.service.price
        super(Payment, self).save(*args, **kwargs)

    def wallet_balance(self):
        payments = Payment.objects.filter(user=self)
        balance = sum([payment.amount for payment in payments if payment.confirmed])
        return balance

    def payment_history(self):
        payments = Payment.objects.filter(user=self)
        for payment in payments:
            payment_history = [
                {
                 'job': payment.job.name,
                 'amount': payment.amount,
                 'timestamp': payment.timestamp,
                 'confirmed': payment.confirmed
                 }
            ]
            return payment_history


class Message(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        ordering = ('timestamp',)



