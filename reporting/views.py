from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F, Max
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta

from sales.models import Sale, SaleItem
from products.models import Product
from customers.models import Customer


@login_required
def reports_dashboard(request):
    """Dashboard principal de relatórios"""
    
    # Período padrão - últimos 30 dias
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Filtros do usuário
    period = request.GET.get('period', '30')
    if period == '7':
        start_date = end_date - timedelta(days=7)
    elif period == '30':
        start_date = end_date - timedelta(days=30)
    elif period == '90':
        start_date = end_date - timedelta(days=90)
    
    context = {
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reporting/dashboard.html', context)


@login_required
def products_report(request):
    """Relatório de produtos mais vendidos"""
    
    # Período
    period = request.GET.get('period', '30')
    end_date = timezone.now().date()
    
    if period == '7':
        start_date = end_date - timedelta(days=7)
    elif period == '30':
        start_date = end_date - timedelta(days=30)
    elif period == '90':
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    # Produtos mais vendidos
    top_products = SaleItem.objects.filter(
        sale__created_at__date__gte=start_date,
        sale__created_at__date__lte=end_date
    ).values(
        'product__title',
        'product__size__name',
        'product__color__name',
        'product__brand__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('unit_price')),
        sales_count=Count('sale', distinct=True)
    ).order_by('-total_quantity')[:20]
    
    # Produtos com baixo estoque
    low_stock_products = Product.objects.filter(
        is_active=True,
        quantity__lte=F('min_stock')
    ).select_related('brand', 'size', 'color')[:20]
    
    # Produtos sem estoque
    out_of_stock = Product.objects.filter(
        is_active=True,
        quantity=0
    ).select_related('brand', 'size', 'color').count()
    
    context = {
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_count': out_of_stock,
    }
    
    return render(request, 'reporting/products.html', context)


@login_required
def sales_report(request):
    """Relatório de vendas por período"""
    
    # Período
    period = request.GET.get('period', '30')
    end_date = timezone.now().date()
    
    if period == '7':
        start_date = end_date - timedelta(days=7)
    elif period == '30':
        start_date = end_date - timedelta(days=30)
    elif period == '90':
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    # Vendas no período
    sales_period = Sale.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    # Totais
    total_sales = sales_period.count()
    total_revenue = sales_period.aggregate(
        total=Sum('final_amount')
    )['total'] or 0
    
    total_discount = sales_period.aggregate(
        total=Sum('discount')
    )['total'] or 0
    
    # Calcular ticket médio
    average_ticket = total_revenue / total_sales if total_sales > 0 else 0
    
    # Vendas por dia
    daily_sales = {}
    for sale in sales_period.values('created_at__date').annotate(
        count=Count('id'),
        revenue=Sum('final_amount')
    ).order_by('created_at__date'):
        daily_sales[sale['created_at__date']] = {
            'count': sale['count'],
            'revenue': sale['revenue'] or 0,
            'average_ticket': (sale['revenue'] or 0) / sale['count'] if sale['count'] > 0 else 0
        }
    
    # Vendas por forma de pagamento
    payment_stats = sales_period.values('payment_method').annotate(
        count=Count('id'),
        revenue=Sum('final_amount')
    ).order_by('-count')
    
    # Vendas por vendedor
    seller_stats = sales_period.values(
        'seller__username',
        'seller__first_name',
        'seller__last_name'
    ).annotate(
        count=Count('id'),
        revenue=Sum('final_amount')
    ).order_by('-revenue')
    
    context = {
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_discount': total_discount,
        'average_ticket': average_ticket,
        'daily_sales': daily_sales,
        'payment_stats': payment_stats,
        'seller_stats': seller_stats,
    }
    
    return render(request, 'reporting/sales.html', context)


@login_required
def stock_report(request):
    """Relatório de estoque atual"""
    
    # Filtros
    category_filter = request.GET.get('category')
    brand_filter = request.GET.get('brand')
    low_stock_only = request.GET.get('low_stock_only')
    
    # Query base
    products = Product.objects.filter(is_active=True).select_related(
        'brand', 'category', 'size', 'color'
    )
    
    # Aplicar filtros
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    if brand_filter:
        products = products.filter(brand_id=brand_filter)
    
    if low_stock_only:
        products = products.filter(quantity__lte=F('min_stock'))
    
    # Estatísticas
    total_products = products.count()
    total_value = products.aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0
    
    low_stock_count = products.filter(quantity__lte=F('min_stock')).count()
    out_of_stock_count = products.filter(quantity=0).count()
    
    # Ordenar produtos
    products = products.order_by('quantity', 'title')
    
    # Para filtros
    from categories.models import Category
    from brands.models import Brand
    
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'categories': categories,
        'brands': brands,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'low_stock_only': low_stock_only,
    }
    
    return render(request, 'reporting/stock.html', context)


@login_required
def customers_report(request):
    """Relatório de clientes"""
    
    # Período
    period = request.GET.get('period', '30')
    end_date = timezone.now().date()
    
    if period == '7':
        start_date = end_date - timedelta(days=7)
    elif period == '30':
        start_date = end_date - timedelta(days=30)
    elif period == '90':
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    # Clientes mais ativos
    top_customers = Customer.objects.annotate(
        total_sales=Count('sale'),
        total_spent=Sum('sale__final_amount'),
        last_purchase=Max('sale__created_at')
    ).filter(
        total_sales__gt=0
    ).order_by('-total_spent')[:20]
    
    # Clientes novos no período
    new_customers = Customer.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).count()
    
    # Total de clientes
    total_customers = Customer.objects.count()
    
    context = {
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'top_customers': top_customers,
        'new_customers': new_customers,
        'total_customers': total_customers,
    }
    
    return render(request, 'reporting/customers.html', context)


@login_required
def dashboard_stats_api(request):
    """API para estatísticas do dashboard"""
    
    # Período
    period = request.GET.get('period', '30')
    end_date = timezone.now().date()
    
    if period == '7':
        start_date = end_date - timedelta(days=7)
    elif period == '30':
        start_date = end_date - timedelta(days=30)
    elif period == '90':
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)
    
    # Vendas no período
    sales_period = Sale.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    # Total de vendas
    total_sales = sales_period.count()
    
    # Faturamento total
    total_revenue = sales_period.aggregate(
        total=Sum('final_amount')
    )['total'] or 0
    
    # Produtos com baixo estoque
    low_stock_count = Product.objects.filter(
        is_active=True,
        quantity__lte=F('min_stock')
    ).count()
    
    # Total de clientes
    total_customers = Customer.objects.count()
    
    # Formatar dados para resposta
    data = {
        'total_sales': total_sales,
        'total_revenue': f"R$ {total_revenue:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        'low_stock': low_stock_count,
        'total_customers': total_customers,
        'period': period,
        'period_text': f"{period} dias"
    }
    
    return JsonResponse(data)
