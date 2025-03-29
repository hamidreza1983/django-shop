from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('list/', ProductsList.as_view(), name='products-list'),

]