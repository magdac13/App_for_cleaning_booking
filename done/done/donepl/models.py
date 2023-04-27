import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import JSONField
from django.contrib.gis.geos import Point

from done.done import settings


# Create your models here.
class Job(models.Model):
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
    price = models.DecimalField(max_digits=8, decimal_places=2)
    order_time = models.DateTimeField(auto_now_add=True)
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class User(models.Model):
    payer_account = 'payer'
    service_assistant_account = 'assistant'
    account_types = [
        (payer_account, _('Get your job done')),
        (service_assistant_account, _('You will be doing the job')),
    ]
    gender_male = 'M'
    gender_female = 'F'
    gender_other = 'O'

    gender_choices = [
        (gender_male, _('Male')),
        (gender_female, _('Female')),
        (gender_other, _('Other')),
    ]

    name = models.CharField(
        max_length=100
    )
    surname = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=100
    )
    home_address = models.CharField(
        max_length=2, choices=gender_choices
    )
    phone_number = models.CharField(
        max_length=100
    )
    email = models.EmailField(
        max_length=100
    )
    password = models.CharField(
        max_length=100
    )
    is_active = models.BooleanField(
        default=True
    )
    account_type = models.CharField(
        choices=account_types, max_length=100
    )
    rating = models.FloatField(
        default=5.0, validators=[
            MinValueValidator(3.0), MaxValueValidator(5.0)
        ]
    )
    user_latitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    user_longitude = models.DecimalField(
        max_digits=18, decimal_places=16, null=True, blank=True
    )
    user_google_api_data = JSONField(null=True, blank=True)
    user_geo_point = Point(user_longitude, user_latitude)
    user_live_address = models.CharField()

    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.gender = random.choice([choice[0] for choice in self.gender_choices])
            super().save(*args, **kwargs)

            self.account_type = random.choice([choice[0] for choice in self.account_types])
            super().save(*args, **kwargs)
            for user in User.objects.all():
                user.rating = random.uniform(3.0, 5.0)
                user.save()




    def wallet_balance(self):
        payments = Payment.objects.filter(user=self)
        balance = sum([payment.amount for payment in payments if payment.confirmed])
        return balance

    def payment_history(self):
        payments = Payment.objects.filter(user=self)
        for payment in payments:
            payment_history = [{'job': payment.job.name, 'amount': payment.amount, 'timestamp': payment.timestamp, 'confirmed': payment.confirmed}]
            return payment_history


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} paid {self.amount} on {self.timestamp}"

    def save(self, *args, **kwargs):
        self.amount = self.job.price
        super(Payment, self).save(*args, **kwargs)


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_received')
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ('timestamp',)