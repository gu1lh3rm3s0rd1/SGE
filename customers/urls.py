from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Lista e CRUD de clientes
    path('', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # APIs para busca
    path('api/search/', views.customer_search_api, name='customer_search_api'),
]
