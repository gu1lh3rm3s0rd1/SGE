from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    # Dashboard principal de relatórios
    path('', views.reports_dashboard, name='dashboard'),
    
    # Relatórios específicos
    path('products/', views.products_report, name='products'),
    path('sales/', views.sales_report, name='sales'),
    path('stock/', views.stock_report, name='stock'),
    path('customers/', views.customers_report, name='customers'),
    
    # API para estatísticas
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
]
