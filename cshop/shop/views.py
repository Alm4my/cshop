from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from shop.models import Category, Product


class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'product_list'  # name of the list as a template variable default to model_list or object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.filter(available=True)
        slug = self.kwargs.get('category_slug')

        if slug:
            context['category'] = get_object_or_404(Category, slug=slug)
            context['product_list'] = Product.objects.filter(
                category=context['category']
            )

        return context
