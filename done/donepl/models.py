import random
from django.contrib.auth.models import User, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from geopy.distance import geodesic
from django.contrib.gis.db import models


# Create your models here.

class Service(models.Model):

    JOBS_CHOICES = (
        ('House Cleaning', 'House Cleaning'),
        ('Handy Man', 'Maintenance requests'),
        ('Car Cleaning', 'Car cleaning services, available at gas station points or by your house'),
        ('Kitchen cleaning', 'Kitchen cleaning services'),
        ('Bath Cleaning', 'Bath cleaning services'),
        ('Window Cleaning', 'Window cleaning services'),
        ('Garage Cleaning', 'Garage cleaning services'),
        ('Cooking', 'Cooking'),
        ('Clothes Washing', 'Clothes Washing'),
        ('Dog Walking', 'Dog Walking'),
        ('Pet Feeding', 'Pet Feeding'),
        ('Dishwashing', 'Dishwashing'),
        ('Lawn Mowing', 'Lawn Mowing'),
        ('Plants Watering', 'Plants Watering'),
    )

    name = models.CharField(
        max_length=200,
        choices=JOBS_CHOICES,
        default='House Cleaning'
    )

    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Worker(models.Model):

    date_of_birth = models.DateField(null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )

    home_address = models.CharField(
        max_length=250, null=True
    )
    phone_number = models.CharField(
        max_length=100, null=True
    )

    rating = models.FloatField(
        default=5.0, validators=[
            MinValueValidator(3.0), MaxValueValidator(5.0)
        ], null=True
    )
    worker_location = models.PointField()

    services = models.ManyToManyField(
        Service, blank=True
    )

    photo = models.ImageField(
        upload_to='profile_photos', blank=True, null=True
    )

    def __str__(self):
        return self.user.first_name + '' + self.user.last_name

    def get_location(self):
        return self.worker_location

    def set_location(self, worker_location):
        self.worker_location = worker_location
        self.save()


class Customer(models.Model):

    date_of_birth = models.DateField(null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    home_address = models.CharField(
        max_length=250, null=True
    )
    phone_number = models.CharField(
        max_length=100, null=True
    )

    rating = models.FloatField(
        default=5.0, validators=[
            MinValueValidator(3.0), MaxValueValidator(5.0)
        ], null=True
    )
    customer_location = models.PointField()

    services = models.ManyToManyField(
        Service, blank=True
    )

    photo = models.ImageField(
        upload_to='profile_photos', blank=True, null=True
    )

    def __str__(self):
        return self.user.first_name + '' + self.user.last_name

    def get_location(self):
        return self.customer_location

    def set_location(self, customer_location):
        self.customer_location = customer_location
        self.save()


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



