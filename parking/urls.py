from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lot/<int:lot_id>/', views.lot_detail, name='lot_detail'),
    path('reserve/<int:spot_id>/', views.reserve_spot, name='reserve_spot'),
    path('accounts/', include('django.contrib.auth.urls')),  # Auth URLs
    path('signup/', views.signup, name='signup'),
    path('payment/<int:reservation_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('logout/', views.logout_view, name='logout'),
]
