#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de teste
"""
import os
import sys
import django

# Setup do Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from brands.models import Brand
from categories.models import Category
from sizes.models import Size
from colors.models import Color
from products.models import Product
from customers.models import Customer

def populate_database():
    print("🚀 Populando banco de dados com dados de teste...")
    
    # Criar Marcas
    print("📝 Criando marcas...")
    brands_data = [
        "Nike", "Adidas", "Zara", "H&M", "C&A",
        "Renner", "Riachuelo", "Hering", "Malwee", "Lacoste"
    ]
    
    for brand_name in brands_data:
        brand, created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={'description': f'Marca {brand_name}'}
        )
        if created:
            print(f"   ✅ Marca criada: {brand_name}")
    
    # Criar Categorias
    print("📝 Criando categorias...")
    categories_data = [
        ("Camisetas", "Camisetas masculinas e femininas"),
        ("Calças", "Calças jeans, sociais e casuais"),
        ("Vestidos", "Vestidos casuais e sociais"),
        ("Shorts", "Shorts e bermudas"),
        ("Blusas", "Blusas femininas"),
        ("Casacos", "Casacos e jaquetas"),
        ("Saias", "Saias curtas e longas"),
        ("Underwear", "Roupas íntimas"),
    ]
    
    for cat_name, cat_desc in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'description': cat_desc}
        )
        if created:
            print(f"   ✅ Categoria criada: {cat_name}")
    
    # Criar Tamanhos
    print("📝 Criando tamanhos...")
    sizes_data = ["PP", "P", "M", "G", "GG", "XGG", "36", "38", "40", "42", "44", "46"]
    
    for size_name in sizes_data:
        size, created = Size.objects.get_or_create(
            name=size_name,
            defaults={'description': f'Tamanho {size_name}'}
        )
        if created:
            print(f"   ✅ Tamanho criado: {size_name}")
    
    # Criar Cores
    print("📝 Criando cores...")
    colors_data = [
        ("Branco", "#FFFFFF"),
        ("Preto", "#000000"),
        ("Azul", "#0000FF"),
        ("Vermelho", "#FF0000"),
        ("Verde", "#00FF00"),
        ("Amarelo", "#FFFF00"),
        ("Rosa", "#FFC0CB"),
        ("Cinza", "#808080"),
        ("Marrom", "#8B4513"),
        ("Roxo", "#800080"),
    ]
    
    for color_name, color_code in colors_data:
        color, created = Color.objects.get_or_create(
            name=color_name,
            defaults={'hex_code': color_code}
        )
        if created:
            print(f"   ✅ Cor criada: {color_name}")
    
    # Criar Produtos
    print("📝 Criando produtos...")
    
    # Buscar dados criados
    brands = list(Brand.objects.all())
    categories = list(Category.objects.all())
    sizes = list(Size.objects.all())
    colors = list(Color.objects.all())
    
    products_data = [
        ("Camiseta Básica Masculina", "123456789", "CAMI001", 29.90, 45.00, 20),
        ("Calça Jeans Feminina", "123456790", "CALCA001", 89.90, 120.00, 15),
        ("Vestido Floral", "123456791", "VEST001", 79.90, 110.00, 10),
        ("Blusa Social Feminina", "123456792", "BLUSA001", 49.90, 75.00, 25),
        ("Bermuda Masculina", "123456793", "BERM001", 39.90, 60.00, 18),
        ("Casaco de Moletom", "123456794", "CASACO001", 89.90, 130.00, 12),
        ("Saia Jeans", "123456795", "SAIA001", 59.90, 85.00, 8),
        ("Camiseta Polo", "123456796", "POLO001", 69.90, 95.00, 22),
        ("Shorts Feminino", "123456797", "SHORT001", 34.90, 50.00, 16),
        ("Jaqueta Jeans", "123456798", "JAQ001", 119.90, 160.00, 7),
    ]
    
    import random
    
    for prod_name, barcode, sku, cost, price, qty in products_data:
        # Selecionar dados aleatórios
        brand = random.choice(brands)
        category = random.choice(categories)
        size = random.choice(sizes)
        color = random.choice(colors)
        
        product, created = Product.objects.get_or_create(
            barcode=barcode,
            defaults={
                'title': prod_name,
                'sku': sku,
                'description': f'Descrição do produto {prod_name}',
                'cost_price': cost,
                'selling_price': price,
                'quantity': qty,
                'min_stock': 5,
                'brand': brand,
                'category': category,
                'size': size,
                'color': color,
                'is_active': True,
            }
        )
        if created:
            print(f"   ✅ Produto criado: {prod_name} - R$ {price}")
    
    # Criar Clientes
    print("📝 Criando clientes...")
    customers_data = [
        ("João Silva", "joao@email.com", "(11) 99999-0001", "123.456.789-01"),
        ("Maria Santos", "maria@email.com", "(11) 99999-0002", "123.456.789-02"),
        ("Pedro Oliveira", "pedro@email.com", "(11) 99999-0003", "123.456.789-03"),
        ("Ana Costa", "ana@email.com", "(11) 99999-0004", "123.456.789-04"),
        ("Carlos Souza", "carlos@email.com", "(11) 99999-0005", "123.456.789-05"),
    ]
    
    for cust_name, cust_email, cust_phone, cust_cpf in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=cust_email,
            defaults={
                'name': cust_name,
                'phone': cust_phone,
                'cpf': cust_cpf,
                'address': 'Rua Exemplo, 123 - São Paulo, SP',
            }
        )
        if created:
            print(f"   ✅ Cliente criado: {cust_name}")
    
    print("\n🎉 Banco de dados populado com sucesso!")
    print(f"📊 Dados criados:")
    print(f"   - {Brand.objects.count()} marcas")
    print(f"   - {Category.objects.count()} categorias")
    print(f"   - {Size.objects.count()} tamanhos")
    print(f"   - {Color.objects.count()} cores")
    print(f"   - {Product.objects.count()} produtos")
    print(f"   - {Customer.objects.count()} clientes")

if __name__ == '__main__':
    populate_database()
