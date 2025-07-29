from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telefone')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name='CPF')
    address = models.TextField(null=True, blank=True, verbose_name='Endereço')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name
