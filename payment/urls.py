from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
]