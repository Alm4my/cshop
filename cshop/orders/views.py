import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import DetailView

from cshop import settings
from .tasks import order_created

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


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


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetail(DetailView):
    model = Order
    template_name = 'admin/orders/order/detail.html'


@method_decorator(staff_member_required, name='get')
class AdminOrderPdf(View):
    def get(self, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs.get('pk'))
        html = render_to_string('orders/order/pdf.html', {'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(f'{settings.STATIC_ROOT}css/pdf.css')])
        return response
