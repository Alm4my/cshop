from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.models import Product
from shop.recommender import Recommender


class CartAddItem(View):
    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        form = CartAddProductForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('cart:cart_detail')


class CartRemoveItem(View):
    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartItemsList(ListView):
    template_name = 'cart/detail.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coupon_apply_form'] = CouponApplyForm()
        r = Recommender()
        cart_products = [item['product'] for item in self.object_list]
        context['recommended_products'] = r.suggest_products_for(cart_products,
                                                                 max_results=4)
        return context

    def get_queryset(self):
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                    'quantity': item['quantity'],
                    'override': True
                })
        return cart
