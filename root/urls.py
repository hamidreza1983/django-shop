from django.urls import path
from .views import *

app_name = 'root'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contactus/',ContactUsView.as_view(), name='contactus'),
    path('about/',AboutUsView.as_view(), name='aboutus'),
]