from django.contrib import admin
from .models import Size


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order', 'name')
