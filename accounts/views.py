from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    FormView,
)
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import City

# Create your views here.
class Login(FormView):
    template_name = 'registrations/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        form = form.cleaned_data
        email = form['email']
        password = form['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'ورود موفقیت آمیز'
            )
            return super().form_valid(form)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'کلمه کاربری یا پسورد اشتباه است',
            )
            return redirect(self.request.path_info)
    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            'داده های ورودی نامعتبر میباشد',
        )
        return redirect(self.request.path_info)
    
class SignUp(CreateView):
    template_name = 'registrations/signup.html'
    form_class = SignUpForm
    
    def form_valid(self, form):
        form.save()
        data = form.cleaned_data
        email = data['email']
        password = data['password1']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
        messages.add_message(
                self.request,
                messages.SUCCESS,
                'ثبت نام موفقیت آمیز . لطفا مشخصات کاربری خود را تکمیل نمایید'
            )
        return redirect(f'/accounts/edit-profile/{user.id}/')

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            'داده های ورودی نامعتبر میباشد',
        )
        return redirect(self.request.path_info)


class LogOut(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(
                self.request,
                messages.SUCCESS,
                'خروج از حساب کاربری با موفقیت انجام شد'
                
            )
        return redirect("/")

class ViewProfile(LoginRequiredMixin, TemplateView):
    template_name = 'registrations/view-profile.html'
    

class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'registrations/edit-profile.html'
    model = Profile
    fields = ['first_name', 'last_name', 'birthday', 'mobile', 'phone', 'card_number', 'id_code']
    success_url = '/accounts/view-profile/'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if kwargs.get("pk") != user.id: # اگر کاربر در حال ویرایش پروفایل خودش نباشد
            messages.error(self.request, "شما مجاز به ویرایش این پروفایل نیستید")
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "پروفایل شما با موفقیت ویرایش شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")# ارورهایی که در ولیدیتور مدل نوشته شده برمیگرداند
        return super().form_invalid(form)

class SetAddressView(LoginRequiredMixin, CreateView):
    template_name = 'registrations/addresses.html'
    form_class = SetAddressForm
    success_url = '/accounts/profile/addresses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        messages.add_message(
                self.request,
                messages.SUCCESS,
                'ثبت آدرس با موفقیت انجام شد'
            )
        return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_id = get_object_or_404(Profile, user=user).id 
        if request.POST.get('profile') != str(profile_id): # اگر کاربر در حال ویرایش پروفایل خودش نباشد
            messages.error(self.request, "شما مجاز به ویرایش این پروفایل نیستید")
        return super().post(request, *args, **kwargs)


    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")
        return redirect(self.request.path_info)
    


def get_cities(request):
    province_id = request.GET.get('province_id')
    print (province_id)
    if province_id:
        cities = City.objects.filter(province=province_id).values('id', 'name')
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)


class ResetPassword(FormView):
    pass

class ResetPasswordDone(TemplateView):
    pass

class ResetPasswordConfirm(FormView):
    pass

class ResetPasswordComplete(TemplateView):
    pass