"""
Script para verificar dados no sistema e testar as estatísticas
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/sge')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from sales.models import Sale, SaleItem
from products.models import Product
from customers.models import Customer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F

def test_dashboard_stats():
    print("🔍 Verificando dados para o dashboard...")
    
    # Período dos últimos 30 dias
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    print(f"📅 Período: {start_date} até {end_date}")
    
    # Vendas
    sales_period = Sale.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    total_sales = sales_period.count()
    total_revenue = sales_period.aggregate(total=Sum('final_amount'))['total'] or 0
    
    print(f"💰 Vendas no período: {total_sales}")
    print(f"💰 Faturamento: R$ {total_revenue:,.2f}")
    
    # Produtos com baixo estoque
    low_stock_count = Product.objects.filter(
        is_active=True,
        quantity__lte=F('min_stock')
    ).count()
    
    print(f"📦 Produtos com baixo estoque: {low_stock_count}")
    
    # Clientes
    total_customers = Customer.objects.count()
    print(f"👥 Total de clientes: {total_customers}")
    
    # Dados gerais
    total_products = Product.objects.filter(is_active=True).count()
    total_all_sales = Sale.objects.count()
    
    print(f"\n📊 Resumo geral:")
    print(f"   - Produtos ativos: {total_products}")
    print(f"   - Total de vendas (histórico): {total_all_sales}")
    print(f"   - Clientes cadastrados: {total_customers}")
    
    return {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'low_stock': low_stock_count,
        'total_customers': total_customers
    }

if __name__ == "__main__":
    stats = test_dashboard_stats()
    print(f"\n✅ Dados carregados com sucesso!")
    print(f"🔗 Teste a API em: http://localhost:8000/reports/api/dashboard-stats/?period=30")
