from io import BytesIO

import weasyprint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from cshop import settings
from cshop.celery import app
from orders.models import Order


@app.task
def payment_completed(order_id):
    """
    Task to send an email notification when an order is successfully created.

    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'Jersey Store - EE Invoice no. 00{order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@cshop.com', [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # send email
    email.send()
