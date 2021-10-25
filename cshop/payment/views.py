import braintree
from django.shortcuts import get_object_or_404, redirect, render

from django.views import View
from django.views.generic import TemplateView

from cshop import settings

from orders.models import Order

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class PaymentProcess(View):
    template_name = 'payment/process.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'client_token': gateway.client_token.generate()})

    def post(self, *args, **kwargs):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.get_total_cost()
        # retrieve nonce
        nonce = self.request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        return redirect('payment:cancelled')


class PaymentDone(TemplateView):
    template_name = 'payment/done.html'


class PaymentCancelled(TemplateView):
    template_name = 'payment/cancelled.html'
