from django.urls import path

from orders.views import OrderCreate

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
]