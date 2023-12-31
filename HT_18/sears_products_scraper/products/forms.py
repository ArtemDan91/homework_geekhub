import re

from django import forms
from django.core.exceptions import ValidationError

from .models import ScrapingTask


def validate_product_ids(value):
    pattern = r'^[A-Za-z0-9]+$'
    products_ids = value.split()
    for product_id in products_ids:
        if not re.match(pattern, product_id):
            raise ValidationError('Invalid ID format')


class ScrapingTaskForm(forms.ModelForm):
    class Meta:
        model = ScrapingTask
        fields = ['product_id']

    product_id = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            'required': 'Please, enter at least one product ID. You can input multiple IDs separated by spaces.',
        }
    )

    def clean_product_id(self):
        products_ids = self.cleaned_data.get('product_id', '').split()

        pattern = r'^[A-Z\d]{8,15}$'

        if not all([re.match(pattern, product_id) for product_id in products_ids]):
            raise ValidationError('Invalid ID format. Please make sure that all entered products IDs are valid.')
        return products_ids

