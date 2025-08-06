from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Product
from .forms import ProductForm, ProductSearchForm
from categories.models import Category
from brands.models import Brand



@login_required
def product_list(request):
    """Lista de produtos com busca e filtros"""
    products = Product.objects.select_related('category', 'brand', 'size', 'color').filter(is_active=True)
    
    # Busca por título ou número de série
    search_title = request.GET.get('title', '').strip()
    search_serie = request.GET.get('serie_number', '').strip()
    category_id = request.GET.get('category', '').strip()
    brand_id = request.GET.get('brand', '').strip()
    
    if search_title:
        products = products.filter(title__icontains=search_title)
    
    if search_serie:
        products = products.filter(
            Q(barcode__icontains=search_serie) | 
            Q(sku__icontains=search_serie)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if brand_id:
        products = products.filter(brand_id=brand_id)
    
    # Ordenar por ID descendente
    products = products.order_by('-id')
    
    # Paginação
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': Category.objects.all().order_by('name'),
        'brands': Brand.objects.all().order_by('name'),
        'search_title': search_title,
        'search_serie': search_serie,
        'selected_category': category_id,
        'selected_brand': brand_id,
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Detalhes do produto"""
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@login_required
def product_create(request):
    """Criar novo produto"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produto "{product.title}" criado com sucesso!')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Novo Produto'}
    return render(request, 'products/product_form.html', context)


@login_required
def product_update(request, pk):
    """Atualizar produto"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produto "{product.title}" atualizado com sucesso!')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form, 
        'product': product,
        'title': f'Editar Produto: {product.title}'
    }
    return render(request, 'products/product_form.html', context)


@login_required
def product_delete(request, pk):
    """Excluir produto"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.title
        product.delete()
        messages.success(request, f'Produto "{product_name}" excluído com sucesso!')
        return redirect('products:product_list')
    
    context = {'product': product}
    return render(request, 'products/product_confirm_delete.html', context)