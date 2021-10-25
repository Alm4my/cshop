from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View

from .tasks import order_created

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


class OrderCreate(View):
    get_template_name = 'orders/order/create.html'
    post_template_name = 'orders/order/created.html'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
        return self.get(request)

    def get(self, request):
        return render(request, self.get_template_name, {'form': OrderCreateForm()})
