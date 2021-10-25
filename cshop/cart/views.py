from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product


class CartAdd(View):
    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        form = CartAddProductForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('cart:cart_detail')


class CartRemove(View):
    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetail(ListView):
    template_name = 'cart/detail.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


