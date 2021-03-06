from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, CharField, EmailField, DateTimeField, BooleanField, ForeignKey, CASCADE, \
    DecimalField, PositiveIntegerField, SET_NULL, IntegerField

from coupons.models import Coupon
from shop.models import Product


class Order(Model):
    first_name = CharField(_('first name'), max_length=100)
    last_name = CharField(_('last name'), max_length=100)
    email = EmailField(_('email'))
    address = CharField(_('address'), max_length=255)
    postal_code = CharField(_('postal code'), max_length=20, default='00225')
    city = CharField(_('city'), max_length=100, default='Abidjan')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    paid = BooleanField(default=False)
    braintree_id = CharField(max_length=150, blank=True)
    discount = IntegerField(default=0, validators=[MinValueValidator(0),
                                                   MaxValueValidator(100)])
    coupon = ForeignKey(Coupon, related_name='orders', null=True, blank=True,
                        on_delete=SET_NULL)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))


class OrderItem(Model):
    order = ForeignKey(Order, related_name='items', on_delete=CASCADE)
    product = ForeignKey(Product, related_name='order_items', on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
