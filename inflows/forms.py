from django import forms
from django.core.exceptions import ValidationError
from . import models
from products.models import Product


class InflowForm(forms.ModelForm):
    # Campo de busca de produto
    product_search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Buscar produto por nome, código de barras ou SKU...',
            'id': 'product-search',
            'autocomplete': 'off'
        }),
        label='Buscar Produto'
    )

    class Meta:
        model = models.Inflow
        fields = ['supplier', 'product', 'quantity', 'description']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={
                'class': 'form-select',
                'id': 'product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '1',
                'placeholder': 'Quantidade recebida'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre esta entrada (opcional)'
            }),
        }
        labels = {
            'supplier': 'Fornecedor',
            'product': 'Produto',
            'quantity': 'Quantidade Recebida',
            'description': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Melhorar a exibição dos produtos no select
        self.fields['product'].queryset = Product.objects.filter(is_active=True).select_related('brand', 'size', 'color')
        self.fields['product'].empty_label = "Selecione um produto"
        
        # Personalizar a exibição dos produtos
        self.fields['product'].label_from_instance = lambda obj: f"{obj.title} - {obj.size} - {obj.color} (Estoque: {obj.quantity})"

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
        return quantity


class QuickInflowForm(forms.Form):
    """Formulário simplificado para entrada rápida de estoque"""
    
    product_search = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite o código de barras ou nome do produto...',
            'autofocus': True,
            'id': 'quick-product-search'
        }),
        label='Produto'
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Quantidade',
            'min': '1'
        }),
        label='Quantidade'
    )
    
    notes = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Observações (opcional)'
        }),
        label='Observações'
    )
