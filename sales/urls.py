from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Lista e detalhes de vendas
    path('', views.sale_list, name='sale_list'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/receipt/', views.sale_receipt, name='sale_receipt'),
    
    # Venda rápida (interface principal)
    path('quick/', views.quick_sale, name='quick_sale'),
    path('quick/process/', views.process_quick_sale, name='process_quick_sale'),
    
    # APIs para busca
    path('api/products/', views.product_search_api, name='product_search_api'),
    path('api/customers/', views.customer_search_api, name='customer_search_api'),
    path('api/customer/add/', views.add_quick_customer, name='add_quick_customer'),
]
