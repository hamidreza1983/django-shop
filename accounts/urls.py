from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('view-profile/', ViewProfile.as_view(), name='view-profile'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('reset-password-done/', ResetPasswordDone.as_view(), name='reset-password-done'),
    path('reset-password-confirm/<str:token>', ResetPasswordConfirm.as_view(), name='reset-password-confirm'),
    path('reset-password-complete/', ResetPasswordComplete.as_view(), name='reset-password-complete'),
]