from django.contrib import admin
from . import models


class OutflowAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'sale', 'created_at', 'updated_at',)
    search_fields = ('product__title', 'description')
    list_filter = ('created_at', 'sale')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(models.Outflow, OutflowAdmin)
