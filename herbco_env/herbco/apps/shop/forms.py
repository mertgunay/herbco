from django import forms

from .models import Item

class ItemCreateForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [
            'image',
            'name',
            'description',
            'price',
            'stock',
            'weight',
            'category',
            'related_product'
        ]
        help_texts = {
            'related_product': 'This is optional. If a product have a relation with other product use this one',
            'weight'         : 'Gram'
        }
