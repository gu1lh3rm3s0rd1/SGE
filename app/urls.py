from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .manual_views import manual_operacao


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/v1/', include('authentication.urls')),

    path('', views.home, name='home'),
    path('', include('suppliers.urls')),
    path('', include('brands.urls')),
    path('', include('categories.urls')),
    path('products/', include('products.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path('sales/', include('sales.urls')),
    path('customers/', include('customers.urls')),
    path('reports/', include('reporting.urls')),
    
    # Manual de operação
    path('manual/', manual_operacao, name='manual_operacao'),
]
