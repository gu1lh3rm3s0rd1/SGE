from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Sale, SaleItem
from outflows.models import Outflow


@receiver(post_save, sender=SaleItem)
def create_outflows_from_sale_items(sender, instance, created, **kwargs):
    """
    Quando um item de venda é criado, verifica se todos os itens da venda
    foram processados e então cria os registros de saída (outflows).
    """
    if created:
        # Usar transaction.on_commit para garantir que seja executado após o commit
        transaction.on_commit(lambda: process_sale_outflows(instance.sale))


def process_sale_outflows(sale):
    """
    Processa a criação de outflows para uma venda específica.
    Evita duplicação verificando se já existem outflows para esta venda.
    """
    # Verifica se já existem outflows para esta venda
    existing_outflows = Outflow.objects.filter(sale=sale)
    if existing_outflows.exists():
        return
    
    # Cria um outflow para cada item da venda
    for item in sale.items.all():
        Outflow.objects.create(
            product=item.product,
            quantity=item.quantity,
            description=f"Venda #{sale.id} - {item.product.title} - Cliente: {sale.customer.name if sale.customer else 'N/A'}",
            sale=sale
        )
