from django.db import models
from django.utils.timezone import now

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    total_spots = models.IntegerField()

    def __str__(self):
        return self.name


class ParkingSpot(models.Model):
    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    spot_number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price of the spot in dollars
    
    def __str__(self):
        return f"Spot {self.id} - Price: ${self.price}"


class Reservation(models.Model):
    user = models.CharField(max_length=100)  # Simplified for now
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Reservation by {self.user} for Spot {self.spot.spot_number}"


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)  # Automatically set when the payment is made
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Payment {self.id} for Reservation {self.reservation.id}"