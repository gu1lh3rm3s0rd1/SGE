from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller', 'final_amount', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at', 'seller')
    search_fields = ('customer__name', 'seller__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SaleItemInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'seller')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('sale__created_at',)
    search_fields = ('product__title', 'sale__id')
    readonly_fields = ('total_price',)
