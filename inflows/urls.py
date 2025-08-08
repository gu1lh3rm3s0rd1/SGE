from django.urls import path
from . import views


urlpatterns = [
    path('inflows/list/', views.InflowListView.as_view(), name='inflow_list'),
    path('inflows/create/', views.InflowCreateView.as_view(), name='inflow_create'),
    path('inflows/<int:pk>/detail/', views.InflowDetailView.as_view(), name='inflow_detail'),

    # APIs REST
    path('api/v1/inflows/', views.InflowCreateListAPIView.as_view(), name='inflow-create-list-api-view'),
    path('api/v1/inflows/<int:pk>/', views.InflowRetrieveAPIView.as_view(), name='inflow-detail-api-view'),
    
    # API para scanner
    path('api/search-product/<str:barcode>/', views.search_product_for_inflow, name='search_product_for_inflow'),
    path('api/save-bulk-inflows/', views.save_bulk_inflows, name='save_bulk_inflows'),
]
