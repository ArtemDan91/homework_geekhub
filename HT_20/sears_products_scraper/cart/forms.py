from django import forms


class EnterProductQuantityToCartForm(forms.Form):
    quantity = forms.IntegerField()