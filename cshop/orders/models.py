from django.db.models import Model, CharField, EmailField, DateTimeField, BooleanField, ForeignKey, CASCADE, \
    DecimalField, PositiveIntegerField

from shop.models import Product


class Order(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField()
    address = CharField(max_length=255)
    postal_code = CharField(max_length=20, default='00225')
    city = CharField(max_length=100, default='Abidjan')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    paid = BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(Model):
    order = ForeignKey(Order, related_name='items', on_delete=CASCADE)
    product = ForeignKey(Product, related_name='order_items', on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
