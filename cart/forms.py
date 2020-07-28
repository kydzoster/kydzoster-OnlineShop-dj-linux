from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # this allows users to select a quantity from 1 to 20
    quantity = forms.TypedChoiceField( choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # this allows to add to existing quantity or override with the new one, widget does not display that to users.
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
