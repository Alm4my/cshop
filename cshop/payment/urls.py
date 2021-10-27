from django.urls import path
from django.utils.translation import gettext_lazy as _
from payment.views import PaymentProcess, PaymentDone, PaymentCancelled

app_name = 'payment'

urlpatterns = [
    path(_('process/'), PaymentProcess.as_view(), name='process'),
    path(_('done/'), PaymentDone.as_view(), name='done'),
    path(_('cancelled/'), PaymentCancelled.as_view(), name='cancelled'),
]
