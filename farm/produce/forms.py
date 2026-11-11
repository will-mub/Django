"""Forms for product registration and stock updates. Validation prevents invalid prices and negative stock values from entering the database."""


from django import forms
from .models import Produce


class ProduceForm(forms.ModelForm):

    class Meta:
        model = Produce

        fields = [
            'name',
            'category',
            'description',
            'unit',
            'selling_price',
            'quantity_in_stock',
            'reorder_level',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter produce name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def clean_selling_price(self):
        price = self.cleaned_data['selling_price']

        if price < 0:
            raise forms.ValidationError(
                'Selling price cannot be negative.'
            )

        return price

    def clean_quantity_in_stock(self):
        quantity = self.cleaned_data['quantity_in_stock']

        if quantity < 0:
            raise forms.ValidationError(
                'Stock cannot be negative.'
            )

        return quantity

    def clean_reorder_level(self):
        level = self.cleaned_data['reorder_level']

        if level < 0:
            raise forms.ValidationError(
                'Reorder level cannot be negative.'
            )

        return level
