from django.urls import path

from cart.views import CartAddItem, CartItemsList, CartRemoveItem

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', CartAddItem.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartRemoveItem.as_view(), name='cart_remove'),
    path('', CartItemsList.as_view(), name='cart_detail'),

]
