# Generated by Django 4.0.2 on 2023-05-17 01:59

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=100)),
                ('home_address', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2)),
                ('phone_number', models.CharField(max_length=100)),
                ('rating', models.FloatField(default=5.0, validators=[django.core.validators.MinValueValidator(3.0), django.core.validators.MaxValueValidator(5.0)])),
                ('customer_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('House cleaning', 'You can choose which rooms you want to clean as well as scope of cleaning'), ('Handy Man', 'Maintenance requests'), ('Car cleaning', 'Car cleaning services, available at gas station points or by your house'), ('Kitchen cleaning', 'Kitchen cleaning services'), ('Bath cleaning', 'Bath cleaning services'), ('Window cleaning', 'Window cleaning services'), ('Garage cleaning', 'Garage cleaning services'), ('Cooking', 'Share your meals with neighbors'), ('Clothes Washing', 'Clothes washing services'), ('Dog walking', 'Get your dog a walking buddy'), ('Pet feeding', 'Feed your pets while not at home'), ('Dishwashing', 'Never get tired of dishwashing again'), ('Lawn mowing', 'Ask your neighbor to mow your lawn'), ('Plants watering', "Don't let your plants dry out")], max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_accepted', models.DateTimeField(null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=100)),
                ('home_address', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2)),
                ('phone_number', models.CharField(max_length=100)),
                ('rating', models.FloatField(default=5.0, validators=[django.core.validators.MinValueValidator(3.0), django.core.validators.MaxValueValidator(5.0)])),
                ('worker_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
                ('services', models.ManyToManyField(blank=True, to='donepl.Service')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.service')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=255)),
                ('hours', models.IntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('worker_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('customer_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.service')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donepl.service')),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='services',
            field=models.ManyToManyField(blank=True, to='donepl.Service'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]