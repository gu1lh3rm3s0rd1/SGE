from django import forms
from django.core.exceptions import ValidationError
from .models import Sale, SaleItem
from products.models import Product
from customers.models import Customer


class SaleForm(forms.ModelForm):
    """Formulário principal para vendas"""
    
    # Campo de busca de cliente
    customer_search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar cliente por nome, email ou telefone...',
            'id': 'customer-search',
            'autocomplete': 'off'
        }),
        label='Cliente'
    )

    class Meta:
        model = Sale
        fields = ['customer', 'discount', 'payment_method', 'notes']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select',
                'id': 'customer-select'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações sobre a venda (opcional)'
            }),
        }
        labels = {
            'customer': 'Cliente',
            'discount': 'Desconto (R$)',
            'payment_method': 'Forma de Pagamento',
            'notes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].empty_label = "Cliente avulso"
        self.fields['customer'].required = False


class SaleItemForm(forms.ModelForm):
    """Formulário para itens da venda"""
    
    # Campo de busca de produto
    product_search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Buscar por código de barras, nome ou SKU...',
            'id': 'product-search',
            'autocomplete': 'off',
            'autofocus': True
        }),
        label='Produto'
    )

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select',
                'id': 'product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '1',
                'value': '1',
                'placeholder': 'Qtd'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Preço unitário'
            }),
        }
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'unit_price': 'Preço Unitário (R$)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas produtos ativos com estoque
        self.fields['product'].queryset = Product.objects.filter(
            is_active=True, 
            quantity__gt=0
        ).select_related('brand', 'size', 'color')
        self.fields['product'].empty_label = "Selecione um produto"
        
        # Personalizar a exibição dos produtos
        self.fields['product'].label_from_instance = lambda obj: f"{obj.title} - {obj.size} - {obj.color} (Estoque: {obj.quantity}) - R$ {obj.sale_price}"

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product and quantity:
            if quantity > product.quantity:
                raise ValidationError(f'Quantidade solicitada ({quantity}) maior que o estoque disponível ({product.quantity}).')
        
        return cleaned_data


class QuickSaleForm(forms.Form):
    """Formulário simplificado estilo calculadora para vendas rápidas"""
    
    # Busca de produto
    product_search = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite o código de barras...',
            'autofocus': True,
            'id': 'barcode-input',
            'autocomplete': 'off'
        }),
        label='Código de Barras'
    )
    
    # Quantidade
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'min': '1',
            'id': 'quantity-input'
        }),
        label='Quantidade'
    )
    
    # Desconto
    discount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'min': '0',
            'step': '0.01',
            'placeholder': '0.00',
            'id': 'discount-input'
        }),
        label='Desconto (R$)'
    )
    
    # Forma de pagamento
    PAYMENT_CHOICES = [
        ('cash', 'Dinheiro'),
        ('card', 'Cartão'),
        ('pix', 'PIX'),
        ('installment', 'Parcelado'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        initial='cash',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'payment-method'
        }),
        label='Pagamento'
    )


class CustomerQuickForm(forms.ModelForm):
    """Formulário rápido para cadastro de cliente durante a venda"""
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
        }
        labels = {
            'name': 'Nome',
            'phone': 'Telefone',
            'email': 'E-mail',
        }
