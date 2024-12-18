# Generated by Django 5.1.2 on 2024-11-20 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.TextField()),
                ('total_spots', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot_number', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.parkinglot')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.parkingspot')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='parking.reservation')),
            ],
        ),
    ]
