from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
from django.views.decorators.http import require_http_methods
import json

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm, QuickSaleForm, CustomerQuickForm
from products.models import Product
from customers.models import Customer


@login_required
def sale_list(request):
    """Lista de vendas"""
    sales = Sale.objects.all().select_related('customer', 'seller').order_by('-id')
    
    # Filtro por período
    date_filter = request.GET.get('date_filter')
    if date_filter:
        if date_filter == 'today':
            from django.utils import timezone
            today = timezone.now().date()
            sales = sales.filter(created_at__date=today)
        elif date_filter == 'week':
            from django.utils import timezone
            from datetime import timedelta
            week_ago = timezone.now().date() - timedelta(days=7)
            sales = sales.filter(created_at__date__gte=week_ago)
    
    context = {
        'sales': sales,
        'date_filter': date_filter,
    }
    return render(request, 'sales/sale_list.html', context)


@login_required
def sale_detail(request, pk):
    """Detalhes da venda"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all().select_related('product__brand', 'product__size', 'product__color')
    
    context = {
        'sale': sale,
        'items': items,
    }
    return render(request, 'sales/sale_detail.html', context)


@login_required
def quick_sale(request):
    """Interface de venda rápida estilo calculadora"""
    if request.method == 'POST':
        return process_quick_sale(request)
    
    form = QuickSaleForm()
    recent_sales = Sale.objects.filter(seller=request.user).order_by('-id')[:5]
    
    context = {
        'form': form,
        'recent_sales': recent_sales,
    }
    return render(request, 'sales/quick_sale.html', context)


@login_required
@require_http_methods(["POST"])
def process_quick_sale(request):
    """Processa uma venda rápida"""
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        customer_id = data.get('customer_id')
        discount = float(data.get('discount', 0))
        payment_method = data.get('payment_method', 'dinheiro')
        notes = data.get('notes', '')
        
        if not items:
            return JsonResponse({'success': False, 'error': 'Nenhum item na venda'})
        
        with transaction.atomic():
            # Criar a venda
            sale = Sale.objects.create(
                seller=request.user,
                customer_id=customer_id if customer_id else None,
                discount=discount,
                payment_method=payment_method,
                notes=notes,
                total_amount=0,  # Será atualizado depois
                final_amount=0   # Será atualizado depois
            )
            
            # Adicionar itens e atualizar estoque
            total_amount = 0
            for item_data in items:
                product = get_object_or_404(Product, id=item_data['product_id'])
                quantity = int(item_data['quantity'])
                unit_price = float(item_data['unit_price'])
                
                # Verificar estoque
                if quantity > product.quantity:
                    return JsonResponse({
                        'success': False, 
                        'error': f'Estoque insuficiente para {product.title}. Disponível: {product.quantity}'
                    })
                
                # Criar item da venda
                sale_item = SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price
                )
                
                # Calcular total do item
                sale_item.total_price = quantity * unit_price
                sale_item.save()
                
                # O estoque será reduzido automaticamente via signal do Outflow
                
                total_amount += quantity * unit_price
            
            # Atualizar total da venda
            sale.total_amount = total_amount
            sale.final_amount = total_amount - discount
            sale.save()
            
            return JsonResponse({
                'success': True, 
                'sale_id': sale.id,
                'total': sale.final_amount,
                'message': f'Venda #{sale.id} realizada com sucesso!'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def product_search_api(request):
    """API para busca de produtos via AJAX"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'products': []})
    
    # Buscar por código de barras, SKU ou nome
    products = Product.objects.filter(
        Q(barcode__icontains=query) |
        Q(sku__icontains=query) |
        Q(title__icontains=query),
        is_active=True,
        quantity__gt=0
    ).select_related('brand', 'size', 'color')[:10]
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'title': product.title,
            'brand': product.brand.name if product.brand else '',
            'size': product.size.name if product.size else '',
            'color': product.color.name if product.color else '',
            'barcode': product.barcode or '',
            'sku': product.sku or '',
            'selling_price': float(product.selling_price),
            'quantity': product.quantity,
            'display_name': f"{product.title} - {product.size} - {product.color}",
            'stock_info': f"Estoque: {product.quantity}"
        })
    
    return JsonResponse({'products': product_list})


@login_required
def customer_search_api(request):
    """API para busca de clientes via AJAX"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'customers': []})
    
    customers = Customer.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(phone__icontains=query)
    )[:10]
    
    customer_list = []
    for customer in customers:
        customer_list.append({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email or '',
            'phone': customer.phone or '',
            'display_name': f"{customer.name} - {customer.phone}"
        })
    
    return JsonResponse({'customers': customer_list})


@login_required
def add_quick_customer(request):
    """Adicionar cliente rapidamente durante a venda"""
    if request.method == 'POST':
        form = CustomerQuickForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'display_name': f"{customer.name} - {customer.phone}"
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def sale_receipt(request, pk):
    """Gerar recibo da venda"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all().select_related('product')
    
    context = {
        'sale': sale,
        'items': items,
    }
    return render(request, 'sales/receipt.html', context)
