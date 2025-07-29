from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Cor')
    hex_code = models.CharField(max_length=7, null=True, blank=True, verbose_name='Código Hex')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Cor'
        verbose_name_plural = 'Cores'

    def __str__(self):
        return self.name
