from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


class CouponApplyView(View):

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        form = CouponApplyForm(self.request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                self.request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                self.request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
