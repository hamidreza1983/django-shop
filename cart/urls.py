from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('update-cart/', UpdateCartView.as_view(), name='update-cart'),
]