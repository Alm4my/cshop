from django.urls import path

from payment.views import PaymentProcess, PaymentDone, PaymentCancelled

app_name = 'payment'

urlpatterns = [
    path('process/', PaymentProcess.as_view(), name='process'),
    path('done/', PaymentDone.as_view(), name='done'),
    path('cancelled/', PaymentCancelled.as_view(), name='cancelled'),
]
