from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from shop.models import Category, Product


class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug')
        if slug:
            context['category'] = get_object_or_404(Category, slug=slug)
            context['product_list'] = Product.objects.filter(
                category=context['category']
            )
            return context
        # no slug (base case)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.filter(available=True)
        return context


class ProductDetail(DetailView):
    template_name = 'shop/product/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['category_list'] = Category.objects.all()
        return context


