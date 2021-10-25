from django.core.mail import send_mail

from cshop.celery import app
from orders.models import Order


@app.task
def order_created(order_id):
    """
    Task to send an email notification when an order is successfully created.

    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f"""Dear {order.first_name}, \n\nYou have successfully placed an order."""
    mail_sent = send_mail(subject, message, 'admil@cshop.com', [order.email])
    return mail_sent
