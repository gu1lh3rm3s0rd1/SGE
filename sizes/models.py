from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='Tamanho')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Tamanho'
        verbose_name_plural = 'Tamanhos'

    def __str__(self):
        return self.name
