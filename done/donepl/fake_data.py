import os
from django.db import connection
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "done.done.settings")
import django

django.setup()
from random import randint
from django.core.management import call_command
from django.contrib.gis.geos import Point
from faker import Faker
import psycopg2
from django.conf import settings
from donepl.models import Worker, Customer, User

fake = Faker()

conn = psycopg2.connect(
    database='done',
    user='postgres',
    password='coderslab',
    host='localhost',
    port=5432
)

cur = connection.cursor()

used_usernames = set()


for i in range(100):
    first_name = fake.name()
    email = fake.email()
    last_name = fake.last_name()
    date_of_birth = fake.date_of_birth()
    home_address = fake.address()
    phone_number = fake.phone_number()
    password = fake.password(length=10)
    while True:

        username = fake.user_name()
        if username not in used_usernames:
            used_usernames.add(username)
            break
    is_superuser = fake.pybool()
    is_staff = fake.pybool()
    is_active = fake.pybool()
    date_joined = fake.date_time_this_year()
    rating = fake.pyfloat(min_value=3.0, max_value=5.0)
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        username=username,
        is_superuser=is_superuser,
        is_staff=is_staff,
        is_active=is_active,
        date_joined=timezone.now(),
    )

    user_id = user.id
    # Create a Point object using the generated coordinates
    worker_location = Point(fake.latlng())
    customer_location = Point(fake.latlng())
    # Convert the Point object to a compatible format
    customer_location_sql = customer_location.wkt
    worker_location_sql = worker_location.wkt

    query1 = """INSERT INTO auth_user(
        first_name, last_name, email, 
        password, username, is_superuser, is_staff,   
        is_active, date_joined) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    query2 = """INSERT INTO donepl_worker(
    date_of_birth, home_address, 
    phone_number, worker_location, 
    rating, user_id)
    VALUES (%s, %s, %s, ST_GeomFromText(%s), %s, %s)
    """

    query3 = """INSERT INTO donepl_customer(
    date_of_birth, home_address, 
    phone_number, customer_location, 
    rating, user_id)
    VALUES(%s, %s, %s, ST_GeomFromText(%s), %s, %s)
    """

    # cur.execute(query1, (first_name, last_name, email, password, username, is_superuser,
                         # is_staff, is_active, date_joined))
    # cur.execute(query2, (date_of_birth, home_address, phone_number,
                         # worker_location_sql, rating, user_id))
    cur.execute(query3, (date_of_birth, home_address, phone_number,
                         customer_location_sql, rating, user_id))
