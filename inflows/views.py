from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
import json
from products.models import Product
from suppliers.models import Supplier
from . import models, forms, serializers


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflows.view_inflow'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        product = self.request.GET.get('product')

        if product:
            queryset = queryset.filter(product__title__icontains=product)

        return queryset


class InflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflows.add_inflow'


class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail.html'
    permission_required = 'inflows.view_inflow'


class InflowCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Inflow.objects.all().order_by('-id')
    serializer_class = serializers.InflowSerializer


class InflowRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Inflow.objects.all().order_by('-id')
    serializer_class = serializers.InflowSerializer


@require_http_methods(["GET"])
@login_required
def search_product_for_inflow(request, barcode):
    """API para buscar produto por código de barras para entrada de estoque"""
    try:
        product = Product.objects.get(barcode=barcode, is_active=True)
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.title,
                'barcode': product.barcode,
                'sku': product.sku or '',
                'current_stock': product.quantity,
                'brand': product.brand.name if product.brand else '',
                'size': product.size.name if product.size else '',
                'color': product.color.name if product.color else '',
                'cost_price': float(product.cost_price),
                'selling_price': float(product.selling_price),
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Produto não encontrado'
        })


@require_http_methods(["POST"])
@login_required
@csrf_exempt
def save_bulk_inflows(request):
    """API para salvar múltiplas entradas de estoque escaneadas"""
    try:
        data = json.loads(request.body)
        products_data = data.get('products', [])
        supplier_id = data.get('supplier_id')
        
        if not products_data:
            return JsonResponse({
                'success': False,
                'error': 'Nenhum produto fornecido'
            })
        
        # Verificar se tem fornecedor padrão ou usar o primeiro disponível
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Fornecedor não encontrado'
                })
        else:
            # Usar primeiro fornecedor disponível ou criar um genérico
            supplier = Supplier.objects.first()
            if not supplier:
                return JsonResponse({
                    'success': False,
                    'error': 'Nenhum fornecedor cadastrado. Cadastre um fornecedor primeiro.'
                })
        
        created_inflows = []
        
        # Usar transação para garantir atomicidade
        with transaction.atomic():
            for product_data in products_data:
                try:
                    product = Product.objects.get(id=product_data['id'])
                    quantity = int(product_data['quantity'])
                    notes = product_data.get('notes', '')
                    
                    # Criar entrada de estoque
                    inflow = models.Inflow.objects.create(
                        supplier=supplier,
                        product=product,
                        quantity=quantity,
                        description=f"Entrada via scanner - {notes}" if notes else "Entrada via scanner"
                    )
                    
                    # Atualizar estoque do produto
                    product.quantity += quantity
                    product.save()
                    
                    created_inflows.append({
                        'id': inflow.id,
                        'product_name': product.title,
                        'quantity': quantity,
                        'new_stock': product.quantity
                    })
                    
                except Product.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'Produto ID {product_data["id"]} não encontrado'
                    })
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'error': f'Quantidade inválida para produto {product_data.get("name", "")}'
                    })
        
        return JsonResponse({
            'success': True,
            'message': f'{len(created_inflows)} entradas criadas com sucesso!',
            'entries': created_inflows,
            'supplier': supplier.name
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })
