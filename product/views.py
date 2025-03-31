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
from django.db.models import Q

# Create your views here.
class ProductsView(ListView):
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
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by('-created_at')[:3]
        context["product_count"] = self.model.objects.all().count()
        return context
    
    def get_queryset(self):       
        categories = self.request.GET.getlist('category')  # گرفتن لیست دسته‌بندی‌ها
        category_detail = self.request.GET.get('detail-category')
        if categories:
            # ساختن شرط OR به صورت داینامیک
            query = Q()
            for category in categories:
                query |= Q(category__id=category)
                query |= Q(category__parent__id=category)  # اضافه کردن هر مقدار با OR
                query |= Q(category__parent__parent__id=category)

            return Products.objects.filter(query)
        if category_detail:
            return Products.objects.filter(category__name=category_detail)
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                return Products.objects.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                pass  # در صورتی که مقدار نامعتبر باشد، فیلتر اعمال نشود
        guarantee = self.request.GET.get('guarantee')
        if guarantee == 'true':
            return Products.objects.filter(has_guarantee=True)
        
        return Products.objects.all()
    
class ProductDetailView(DetailView):
    template_name = 'product/product.html'
    model = Products
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

