from django.forms import Form, TypedChoiceField, BooleanField, HiddenInput
from django.utils.translation import gettext_lazy as _

# limits max product to 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(Form):
    quantity = TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                label=_('Quantity'))
    override = BooleanField(required=False, initial=False, widget=HiddenInput)
