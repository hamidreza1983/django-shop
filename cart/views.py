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
import uuid



class CartView(TemplateView):
    template_name = 'carts/cart.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cart = self.request.session.get('cart', {})
    #     if cart:
    #         product_list = [get_object_or_404(Products, pk=key) for key in cart.keys()]
    #         for key, value in cart.items():
    #             product = Products.objects.get(id=key)
    #             quantity = int(value['quantity'])
    #             guarantee_mounts = value['guarantee']
    #             if guarantee_mounts == '0':
    #                 guarantee = None
    #             else:
    #                 guarantee = Guarantee.objects.get(id=guarantee_mounts)
    #             if guarantee:
    #                 price_increase = int(guarantee.price_increase)
    #                 total_product_price = int(product.price) + (int(product.price) * price_increase/100) * quantity   


    #         context['product_list'] = product_list
            
    #     return context

import uuid
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from product.models import Products, Guarantee  # اطمینان از ایمپورت مدل‌های مربوطه


# به ازای تعداد جدید از صفحه آپدیت کارت کار باقی مونده
class AddToCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        g_mount = request.GET.get('g_mount')
        color = request.GET.get("color") if request.GET.get("color") != '' else 'تک رنگ'

        if not pid:
            messages.error(request, 'محصول نامعتبر است.')
            return redirect("product:products")

        # دریافت اطلاعات محصول
        product = get_object_or_404(Products, id=pid)

        # دریافت اطلاعات گارانتی
        guarantee = get_object_or_404(Guarantee, mounts=g_mount) if g_mount != '0' else 0

        # محاسبه قیمت نهایی محصول بر اساس تخفیف و گارانتی
        increase_price_with_guarantee = (product.price * guarantee.price_increase / 100) if guarantee != 0 else 0
        price_with_discount = product.get_discounted_price()
        product_discount = product.discount_price
        product_price = increase_price_with_guarantee + int(price_with_discount)


        cart = request.session.get('cart', {})
        # بررسی اینکه آیا محصول با همان مشخصات قبلاً در سبد خرید هست یا نه
        found = False
        #print (cart.items())
        for key, item in cart.items():
            if item['pid'] == int(pid) and item['color'] == color and item['guarantee'] == g_mount:
                cart[key]['quantity'] += 1  # افزایش تعداد
                cart[key]['final_price'] = cart[key]['quantity'] * product_price
                found = True
                break

        if not found:
            # ایجاد شناسه تصادفی برای محصول جدید
            unique_id = str(uuid.uuid4())[:8]
            cart[unique_id] = {
                'pid': product.id,
                'title': product.name,  # نام محصول
                'image': product.image.url if product.image else None,
                'price': product.price,
                'final_price': product_price,
                'quantity': 1,
                'guarantee': g_mount,
                'color': color,
                'product_discount': product_discount,
            }
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'محصول به سبد خرید شما اضافه شد')
        return redirect("product:product-detail", pk=pid)


class UpdateCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")

    def post(self, request, *args, **kwargs):
        print (request.POST)
        order_numbers = []
        product_ids = []
        
        cart = request.session.get('cart', {})
        product_list = [get_object_or_404(Products, pk=key['pid']) for key in cart.values()]
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
