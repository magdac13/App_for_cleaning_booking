# Generated by Django 4.0.2 on 2023-05-17 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donepl', '0003_alter_customer_home_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='gender',
        ),
        migrations.AlterField(
            model_name='customer',
            name='home_address',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='worker',
            name='home_address',
            field=models.CharField(max_length=250),
        ),
    ]