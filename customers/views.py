from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    """Lista de clientes"""
    search = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    customers = customers.order_by('name')
    
    context = {
        'customers': customers,
        'search': search,
    }
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_detail(request, pk):
    """Detalhes do cliente"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # Buscar vendas do cliente
    from sales.models import Sale
    sales = Sale.objects.filter(customer=customer).order_by('-created_at')[:10]
    
    context = {
        'customer': customer,
        'sales': sales,
    }
    return render(request, 'customers/customer_detail.html', context)


@login_required
def customer_create(request):
    """Criar novo cliente"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Cliente "{customer.name}" criado com sucesso!')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Novo Cliente',
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_update(request, pk):
    """Atualizar cliente"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Cliente "{customer.name}" atualizado com sucesso!')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'title': f'Editar Cliente: {customer.name}',
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_delete(request, pk):
    """Excluir cliente"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, f'Cliente "{customer_name}" excluído com sucesso!')
        return redirect('customers:customer_list')
    
    context = {
        'customer': customer,
    }
    return render(request, 'customers/customer_confirm_delete.html', context)


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
