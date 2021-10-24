from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop.views import ProductList, ProductDetail

app_name = 'shop'

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<slug:category_slug>/', ProductList.as_view(), name='product_list_by_category'),
    path('<int:pk>/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)