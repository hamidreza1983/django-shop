from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView
)
from django.contrib import messages
from product.models import *



class CartView(TemplateView):
    template_name = 'carts/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        if cart:
            product_list = [get_object_or_404(Products, pk=key) for key in cart.keys()]
            context['product_list'] = product_list
            print(self.request.session.get('cart', {}))
        return context



class AddToCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        # del request.session["cart"]
        # request.session.modified = True
        pid = request.GET.get('pid')
        gid = request.GET.get('gid', '0')  # اگر گارانتی انتخاب نشد، مقدار 0 قرار داده شود
        color = request.GET.get("color", "تک رنگ")
        if not pid:  # بررسی مقدار معتبر بودن pid
            messages.error(request, 'محصول نامعتبر است.')
            return redirect("product:products")  # هدایت به لیست محصولات (یا هر جای مناسب)

        cart = request.session.get('cart', {})  # اگر cart وجود نداشت، مقدار پیش‌فرض {}

        if pid in cart:
            cart[pid]['quantity'] = "1"
            cart[pid]['guarantee'] = gid
            cart[pid]['color'] = color
        else:
            cart[pid] = {'quantity': 1, 'guarantee': gid, 'color': color}

        request.session['cart'] = cart
        request.session.modified = True
        print (request.session['cart'])
        messages.success(request, 'محصول به سبد خرید شما اضافه شد')
        return redirect("product:product-detail", pk=pid)


class UpdateCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")

    def post(self, request, *args, **kwargs):
        order_numbers = []
        product_ids = []
        
        cart = request.session.get('cart', {})
        product_list = [get_object_or_404(Products, pk=key) for key in cart.keys()]
        # Collect product ids and their corresponding quantities
        for product in product_list:
            quantity = request.POST.get(f"order-number-{product.id}", 1)  # Default to 1 if not set
            product_ids.append(product.id)
            order_numbers.append(quantity)

        # Update the cart with the new quantities
        for product_id, quantity in zip(product_ids, order_numbers):
            cart[str(product_id)]['quantity'] = quantity

        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'سبد خرید شما با موفقیت بروزرسانی شد')
        return redirect("cart:cart")
