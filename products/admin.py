from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'size', 'color', 'barcode', 'quantity', 'selling_price', 'is_low_stock', 'is_active')
    list_filter = ('brand', 'category', 'size', 'color', 'is_active', 'created_at')
    search_fields = ('title', 'barcode', 'sku')
    list_editable = ('quantity', 'selling_price', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'profit_margin')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'category', 'brand', 'description', 'is_active')
        }),
        ('Identificação', {
            'fields': ('barcode', 'sku')
        }),
        ('Características', {
            'fields': ('size', 'color')
        }),
        ('Preços', {
            'fields': ('cost_price', 'selling_price', 'profit_margin')
        }),
        ('Estoque', {
            'fields': ('quantity', 'min_stock')
        }),
        ('Imagem', {
            'fields': ('image',)
        }),
        ('Controle', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Estoque Baixo'
