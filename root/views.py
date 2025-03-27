from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
)


class HomeView(TemplateView):
    template_name = 'root/index.html'

class ContactUsView(FormView):
    template_name = 'root/contactus.html'
    success_url = '/contactus/'
    form_class = ContactUsForm

    def form_valid(self, form):
        # Process the form data
        # Send email or save to database
        return super().form_valid(form)