from django import forms
from . import models
from sizes.models import Size
from colors.models import Color


class ProductForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos específicos com placeholders úteis
        self.fields['barcode'].widget.attrs.update({
            'placeholder': 'Digite ou escaneie o código de barras',
            'class': 'form-control form-control-lg'
        })

    class Meta:
        model = models.Product
        fields = [
            'title', 'category', 'brand', 'size', 'color',
            'barcode', 'sku', 'cost_price', 'selling_price', 
            'min_stock', 'description', 'image', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ex: Camiseta Básica'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'barcode': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Digite ou escaneie o código'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código interno (opcional)'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01', 
                'min': '0',
                'placeholder': '0.00'
            }),
            'min_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '5'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição adicional do produto (opcional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Nome do Produto *',
            'category': 'Categoria *',
            'brand': 'Marca *',
            'size': 'Tamanho *',
            'color': 'Cor *',
            'barcode': 'Código de Barras',
            'sku': 'SKU (Código Interno)',
            'cost_price': 'Preço de Custo *',
            'selling_price': 'Preço de Venda *',
            'min_stock': 'Estoque Mínimo',
            'description': 'Descrição',
            'image': 'Foto do Produto',
            'is_active': 'Produto Ativo',
        }

    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get('cost_price')
        selling_price = cleaned_data.get('selling_price')
        
        if cost_price and selling_price:
            if selling_price <= cost_price:
                raise forms.ValidationError(
                    'O preço de venda deve ser maior que o preço de custo.'
                )
        
        return cleaned_data


class ProductSearchForm(forms.Form):
    """Formulário para busca rápida de produtos"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Buscar por nome, código de barras ou SKU...',
            'autofocus': True
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        required=False,
        empty_label="Todos os tamanhos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        required=False,
        empty_label="Todas as cores",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        from categories.models import Category
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
