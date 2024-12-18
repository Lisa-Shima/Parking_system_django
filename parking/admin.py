from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import ParkingLot, ParkingSpot, Reservation, Payment

admin.site.register(ParkingLot)
admin.site.register(ParkingSpot)
admin.site.register(Reservation)
admin.site.register(Payment)
