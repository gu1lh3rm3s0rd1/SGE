from django.contrib import admin
from .models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'description')
    search_fields = ('name',)
    list_filter = ('created_at',)
