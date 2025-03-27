from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
)
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import City
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from threading import Thread
from .concurrency_processing import send_email
from django.contrib.auth.password_validation import validate_password

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

    def post(self, request, *args, **kwargs):
        data = request.POST
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            messages.add_message(
                self.request,
                messages.ERROR,
                'این ایمیل قبلا ثبت نام شده است'
            )
            return redirect(self.request.path_info)
        return super().post(request, *args, **kwargs)
    
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
            'پسورد باید با حروف لاتین، 8 کارکتر ، ترکیبی از حروف بزرگ و کوچک و علائم باشد',
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
    

class EditProfile(LoginRequiredMixin, TemplateView):
    template_name = 'registrations/edit-profile.html'
    success_url = '/accounts/view-profile/'
    form_class = EditProfileForm
   
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if kwargs.get("pk") != user.id: # اگر کاربر در حال ویرایش پروفایل خودش نباشد
            messages.error(self.request, "شما مجاز به ویرایش این پروفایل نیستید")
            return redirect('/')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        mobile = profile.mobile
        id_code = profile.id_code
        if mobile == '' and id_code == '':
            form = self.form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(self.request, "پروفایل شما با موفقیت ویرایش شد.")
                return redirect(self.success_url)
            else:
                messages.error(self.request, "کد ملی یا موبایل تکراری میباشد")
                return redirect(request.path_info)
        elif request.POST.get('mobile') != mobile:
            messages.error(self.request, "موبایل قابلیت ویرایش مجدد ندارد")
            return redirect(request.path_info)
        elif request.POST.get('id_code') != id_code:
            messages.error(self.request, "کد ملی قابلیت ویرایش مجدد ندارد")
            return redirect(request.path_info)
        else:
            form = self.form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(self.request, "پروفایل شما با موفقیت ویرایش شد.")
                return redirect(self.success_url)
            else:
                messages.error(self.request, "کد ملی یا موبایل تکراری میباشد")
                return redirect(request.path_info)
  
          
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
    if province_id:
        cities = City.objects.filter(province=province_id).values('id', 'name')
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)


class ResetPassword(FormView):
    success_url = '/accounts/reset-password-done/'
    template_name = 'registrations/forget-password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = self.get_token_for_user(user)
            t1 = Thread(target=send_email, args=('email/email.html', user, token, "admin@my-site.com", user.email))
            t1.start()
            # send email with token
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'ایمیل بازیابی رمز عبور ارسال شد'
            )
            return super().form_valid(form)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'این ایمیل در سیستم وجود ندارد'
            )
            return redirect(self.request.path_info)
        
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ResetPasswordDone(TemplateView):
    template_name = 'registrations/forget-password-done.html'

class ResetPasswordConfirm(FormView):
    template_name = 'registrations/forget-password-confirm.html'
    form_class = ResetPasswordConfirmForm
    success_url = '/accounts/reset-password-complete/'

    def form_valid(self, form):
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 == password2:
            try:
                validate_password(password1)
            except Exception as e:
                messages.error(self.request, "پسورد باید 8 کارکتر شامل حروف بزرگ و کوچک و علائم باشد  ")
                return redirect(self.request.path_info)
            token = self.kwargs.get('token')
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = User.objects.get(id=user_id)
                user.set_password(password1)
                user.save()
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    'رمز عبور با موفقیت تغییر یافت'
                )
                return super().form_valid(form)
            except Exception as e:
                messages.error(self.request, "توکن منقضی شده اسن  ")
                return redirect('/accounts/reset-password/')
        else:
            messages.error(self.request, "پسوردها با هم مطابقت ندارند")
            return redirect(self.request.path_info)

class ResetPasswordComplete(TemplateView):
    template_name = 'registrations/forget-password-complete.html'

class ChangePassword(LoginRequiredMixin, FormView):
    template_name = 'registrations/change-password.html'
    form_class = ChangePasswordForm
    success_url = '/accounts/view-profile/'

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        user = self.request.user
        if not user.check_password(old_password):
            messages.error(self.request, "پسورد قدیمی صحیح نمیباشد")
            return redirect(self.request.path_info)
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 == password2:
            try:
                validate_password(password1)
            except Exception as e:
                messages.error(self.request, "پسورد باید 8 کارکتر شامل حروف بزرگ و کوچک و علائم باشد  ")
                return redirect(self.request.path_info)
            user.set_password(password1)
            user.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'رمز عبور با موفقیت تغییر یافت'
            )
            return super().form_valid(form)
        else:
            messages.error(self.request, "پسوردها با هم مطابقت ندارند")
            return redirect(self.request.path_info)
        
    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")
        return redirect(self.request.path_info)