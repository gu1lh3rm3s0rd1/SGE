from django.db import models
from categories.models import Category
from brands.models import Brand
from sizes.models import Size
from colors.models import Color


class Product(models.Model):
    # Informações básicas
    title = models.CharField(max_length=500, verbose_name='Nome do Produto')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Categoria')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name='Marca')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    
    # Código de barras (essencial para loja de roupas)
    barcode = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Código de Barras')
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='SKU')
    
    # Características específicas de roupas
    size = models.ForeignKey(Size, on_delete=models.PROTECT, related_name='products', verbose_name='Tamanho', default=1)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='products', verbose_name='Cor', default=1)
    
    # Preços
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Custo')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Venda')
    
    # Estoque
    quantity = models.IntegerField(default=0, verbose_name='Quantidade em Estoque')
    min_stock = models.IntegerField(default=5, verbose_name='Estoque Mínimo')
    
    # Foto do produto (opcional, mas muito útil)
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Foto do Produto')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    # Controle de datas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', 'size__order', 'color__name']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        # Garante que não haverá duplicação de produto com mesmo tamanho e cor
        unique_together = ['title', 'brand', 'size', 'color']

    def __str__(self):
        return f"{self.title} - {self.size} - {self.color}"
    
    @property
    def is_low_stock(self):
        """Verifica se o produto está com estoque baixo"""
        return self.quantity <= self.min_stock
    
    @property
    def profit_margin(self):
        """Calcula a margem de lucro"""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0
