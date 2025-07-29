from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Formulário para cadastro/edição de clientes"""
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'cpf', 'address', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do cliente',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'name': 'Nome',
            'email': 'E-mail',
            'phone': 'Telefone',
            'cpf': 'CPF',
            'address': 'Endereço',
            'birth_date': 'Data de Nascimento',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar se já existe outro cliente com este email
            existing_customer = Customer.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None)
            if existing_customer.exists():
                raise forms.ValidationError('Já existe um cliente cadastrado com este e-mail.')
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remover caracteres especiais
            clean_cpf = ''.join(filter(str.isdigit, cpf))
            if len(clean_cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
            
            # Verificar se já existe outro cliente com este CPF
            existing_customer = Customer.objects.filter(cpf=cpf).exclude(id=self.instance.id if self.instance else None)
            if existing_customer.exists():
                raise forms.ValidationError('Já existe um cliente cadastrado com este CPF.')
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remover caracteres especiais para validação
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                raise forms.ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        return phone


class CustomerSearchForm(forms.Form):
    """Formulário de busca de clientes"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome, e-mail ou telefone...',
            'autocomplete': 'off'
        }),
        label='Buscar Cliente'
    )
