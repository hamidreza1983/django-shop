from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    FormView,
)

# Create your views here.
class Login(TemplateView):
    template_name = 'registrations/login.html'
    #form_class = None

class SignUp(CreateView):
    template_name = 'signup.html'
    form_class = None

class LogOut(TemplateView):
    pass

class ViewProfile(UpdateView):
    template_name = 'view_profile.html'
    form_class = None

class ResetPassword(FormView):
    pass

class ResetPasswordDone(TemplateView):
    pass

class ResetPasswordConfirm(FormView):
    pass

class ResetPasswordComplete(TemplateView):
    pass