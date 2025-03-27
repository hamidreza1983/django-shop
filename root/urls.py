from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contactus/',ContactUsView.as_view(), name='contactus'),
]