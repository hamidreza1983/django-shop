from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
)
from django.contrib import messages
from .forms import *


class HomeView(TemplateView):
    template_name = 'root/index.html'


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