from faker import Faker
import psycopg2
from oauthlib.uri_validate import host

fake = Faker()

conn = psycopg2.connect(
    database='done',
    user='postgres',
    password='coderslab',
    host='localhost',
    port=5432
)

cur = conn.cursor()

for i in range(100):
    name = fake.name()
    email = fake.email()
    surname = fake.surname()
    date_of_birth = fake.date_of_birth()
    home_address = fake.address()
    phone_number = fake.phone_number()

    password = fake.password(length=10)
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
