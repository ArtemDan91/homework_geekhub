import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea

from .models import ScrapingTask


class ScrapingTaskForm(forms.ModelForm):
    class Meta:
        model = ScrapingTask
        fields = ['products_ids_list']
        widgets = {
            'products_ids_list': Textarea(),
        }
        error_messages = {
            'products_ids_list': {
                'required': 'Please, enter at least one product ID. You can input multiple IDs separated by spaces.',
            },
        }


    def clean_products_ids_list(self):
        products_ids_list = self.cleaned_data.get('products_ids_list', '').split()

        pattern = r'^[A-Z\d]{8,20}$'

        if not all([re.match(pattern, product_id) for product_id in products_ids_list]):
            raise ValidationError('Invalid ID format. Please make sure that all entered products IDs are valid.')
        return products_ids_list

