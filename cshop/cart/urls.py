from django.urls import path

from cart.views import CartAdd, CartDetail, CartRemove

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartRemove.as_view(), name='cart_remove'),
    path('', CartDetail.as_view(), name='cart_detail'),

]
