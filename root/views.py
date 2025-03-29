from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
)
from django.contrib import messages
from .forms import *
from product.models import Products
from blog.models import Blog


class HomeView(TemplateView):
    template_name = 'root/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_products"] = Products.objects.all().order_by("-total_favorites")[:4]
        context["discounted_products"] = Products.objects.all().order_by("discount_price")[:4]
        context["popular_products"] = Products.objects.all().order_by("total_views")[:4]
        context["best_selling_products"] = Products.objects.all().order_by("total_sold")[:12]

        return context



class ContactUsView(CreateView):
    model = ContactUs
    fields = ['fullname', 'email', 'phone', 'subject', 'message']
    template_name = 'root/contact.html'
    success_url = '/contactus/'

    def form_valid(self, form):
        messages.success(self.request, 'پیام شما با موفقیت دریافت شد . بزودی با شما تماس خواهیم گرفت')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال اطلاعات . لطفا دوباره تلاش کنید')
        return super().form_invalid(form)
    
class AboutUsView(TemplateView):
    template_name = 'root/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.all()
        return context
    
class FaqView(TemplateView):
    template_name = 'root/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Faq.objects.filter(status=True)
        return context