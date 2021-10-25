from django.urls import path

from orders.views import OrderCreate, AdminOrderDetail

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('admin/order/<int:pk>', AdminOrderDetail.as_view(), name='admin_order_detail'),
]
