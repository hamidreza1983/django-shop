from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from product.models import *
import uuid
from accounts.models import Profile, UserAddress
from cart.models import Cart, OrderItems, Status


class  PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/thankyou.html'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        status = Status.objects.get(id=1)
        profile = Profile.objects.get(user=request.user)
        if cart:
            cart_order = Cart.objects.create(profile=profile, 
                                             status=status, 
                                             total_price=request.session['total_price'], 
                                             total_discount=request.session['total_discount_price'], 
                                             total_payment=request.session['payment_price'],
                                             )
            for detail in cart.values():
                print (detail)
                break
                OrderItems.objects.create(cart=cart_order,
                                          product=Products.objects.get(id=detail['pid']),
                                          quantity=detail['quantity'],
                                          color=detail['color'],
                                          guarantee=detail['guarantee'],
                                          )
            # request.session['cart'] = {}
            # request.session['total_price'] = 0
            # request.session['total_discount_price'] = 0
            # request.session['payment_price'] = 0
            # request.session.modified = True

        return super().get(request, *args, **kwargs)

# Create your views here.
