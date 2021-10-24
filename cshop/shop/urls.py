from django.urls import path

from shop.views import ProductList

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<slug:category_slug>/', ProductList.as_view(), name='product_list_by_category'),
]
