from django.shortcuts import render, get_object_or_404
from .models import ParkingLot, ParkingSpot, Reservation
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Reservation, Payment, ParkingLot, ParkingSpot
from django.contrib.auth import logout as auth_logout


def home(request):
    # List all parking lots
    parking_lots = ParkingLot.objects.all()
    payments = Payment.objects.all()
    
    amount_paid = 0
    for payment in payments:
        amount_paid += payment.amount
        
    reservations = Reservation.objects.all().count()
    parking_spots_count = ParkingSpot.objects.all().count()
    
    return render(request, 'parking/home.html', {'parking_lots': parking_lots, 'amount_paid': amount_paid, "reservations": reservations, "parking_lots_count": parking_lots.count(), "parking_spots_count": parking_spots_count})



def lot_detail(request, lot_id):
    # Show details of a specific parking lot, including available spots
    parking_lot = get_object_or_404(ParkingLot, id=lot_id)
    available_spots = ParkingSpot.objects.filter(lot=parking_lot, is_available=True)
    return render(request, 'parking/lot_detail.html', {'parking_lot': parking_lot, 'available_spots': available_spots})


@login_required
def reserve_spot(request, spot_id):
    spot = get_object_or_404(ParkingSpot, id=spot_id)
    if request.method == 'POST':
        spot.is_available = False
        spot.save()
        # Create a reservation
        reservation = Reservation.objects.create(
            user=request.user.username,  # Use the logged-in user's username
            spot=spot,
            start_time=now(),
            end_time=now()
        )
        # return render(request, 'parking/reservation_success.html', {'reservation': reservation})
        return redirect('payment', reservation_id=reservation.id)
    return render(request, 'parking/reserve_spot.html', {'spot': spot})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def payment(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    # Ensure reservation has an associated parking spot with a price
    parking_spot = reservation.spot  # Assuming 'spot' is the relationship to ParkingSpot

    if request.method == 'POST':
        # Step 1: Create a Stripe Checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f"Reservation {reservation.id}",
                            },
                            'unit_amount': int(parking_spot.price * 100),  # Convert price to cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/payment/success/'),
                cancel_url=request.build_absolute_uri('/payment/cancel/'),
            )

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'parking/payment_error.html', {'error': str(e)})

    return render(request, 'parking/payment.html', {'reservation': reservation})



def payment_success(request):
    return render(request, 'parking/payment_success.html')


def payment_cancel(request):
    return render(request, 'parking/payment_cancel.html')

def logout_view(request):
    auth_logout(request)  # Logs the user out
    return redirect('home')