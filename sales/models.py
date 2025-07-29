from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Dinheiro'),
        ('card', 'Cartão'),
        ('pix', 'PIX'),
        ('installment', 'Parcelado'),
    ]
    
    # Informações da venda
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Cliente')
    seller = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Vendedor')
    
    # Valores
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Desconto')
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Final')
    
    # Pagamento
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='Forma de Pagamento')
    installments = models.IntegerField(default=1, verbose_name='Parcelas')
    
    # Observações
    notes = models.TextField(null=True, blank=True, verbose_name='Observações')
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f"Venda #{self.id} - R$ {self.final_amount}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Venda')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produto')
    quantity = models.IntegerField(verbose_name='Quantidade')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Total')

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'

    def __str__(self):
        return f"{self.product} - Qtd: {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
