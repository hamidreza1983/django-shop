from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView
)
from .models import *
from .forms import *
from accounts.models import Profile, User
from django.contrib import messages

# Create your views here.
class Products(ListView):
    model = Products
    template_name = 'product/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by('-created_at')[:3]
        context["product_count"] = self.model.objects.all().count()
        return context
    

class ProductsList(ListView):
    model = Products
    template_name = 'product/products-list.html'
    context_object_name = 'products'