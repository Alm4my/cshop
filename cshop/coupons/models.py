from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, CharField, DateTimeField, IntegerField, BooleanField


class Coupon(Model):
    code = CharField(max_length=50, unique=True)
    valid_from = DateTimeField()
    valid_to = DateTimeField()
    discount = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = BooleanField()

    def __str__(self):
        return self.code
