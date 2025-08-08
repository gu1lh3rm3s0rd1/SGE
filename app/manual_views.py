from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import markdown


@login_required
def manual_operacao(request):
    """Página do manual de operação do sistema"""
    
    # Conteúdo do manual em markdown
    manual_content = """
# 📚 Manual de Operação - Sistema SGE
**Sistema de Gestão de Estoque e Vendas**

---

## 🎯 **O QUE É ESTE SISTEMA?**

Este sistema ajuda você a:
- ✅ **Controlar seu estoque** (saber quantos produtos você tem)
- ✅ **Fazer vendas rapidamente** com código de barras
- ✅ **Cadastrar produtos novos** facilmente
- ✅ **Receber mercadorias** dos fornecedores

**É MUITO FÁCIL!** Você só precisa de um **leitor de código de barras USB** (que funciona como um teclado).

---

## 🏪 **COMO FAZER UMA VENDA RÁPIDA**

### **PASSO 1: Acesse a Venda Rápida**
1. Clique no menu lateral esquerdo
2. Procure por **"Venda Rápida"** (tem um ícone de calculadora 🧮)
3. Clique nele

### **PASSO 2: Escolha o Cliente**
1. Veja o campo **"Cliente"** no topo
2. Digite o nome do cliente OU
3. Deixe em branco se for venda sem cadastro

### **PASSO 3: Adicione Produtos com Scanner**
1. **PEGUE SEU LEITOR DE CÓDIGO DE BARRAS**
2. Coloque o cursor no campo **"Buscar Produto"**
3. **ESCANEIE** o código de barras do produto
4. **MÁGICA!** 🎯 O produto aparece automaticamente na lista

**➡️ Repita para cada produto que o cliente quer comprar**

### **PASSO 4: Conferir a Venda**
- **Lista de produtos**: Aparece do lado esquerdo
- **Total da venda**: Aparece grande do lado direito
- **Se errou algo**: Clique no "X" vermelho para remover

### **PASSO 5: Finalizar a Venda**
1. Confira se está tudo certo
2. Clique no botão verde **"Finalizar Venda"**
3. **PRONTO!** 🎉 Venda realizada!

---

## 📦 **COMO RECEBER MERCADORIA (ENTRADA DE ESTOQUE)**

### **QUANDO USAR:**
- Quando chegam produtos do fornecedor
- Quando você compra mercadoria nova
- Para conferir se chegou tudo certo

### **PASSO 1: Acesse Entradas de Estoque**
1. Menu lateral → **"Entradas"** (ícone de caminhão 🚚)
2. Clique em **"Cadastrar Entrada"**

### **PASSO 2: Scanner de Conferência**
1. **PEGUE SEU LEITOR DE CÓDIGO DE BARRAS**
2. Clique no campo grande **"Escaneie os Produtos"**
3. **ESCANEIE** cada produto que chegou
4. **VEJA A MÁGICA!** 📋 Cada produto vai aparecendo na lista

### **PASSO 3: Verificar Quantidades**
- Se chegaram **2 unidades** do mesmo produto, escaneie **2 vezes** OU
- Clique no ícone de **lápis** ✏️ para ajustar a quantidade

### **PASSO 4: Escolher Fornecedor**
1. No lado direito, escolha quem entregou a mercadoria
2. Se não souber, deixe em branco (sistema escolhe automaticamente)

### **PASSO 5: Finalizar Entrada**
1. Confira a lista de produtos
2. Veja o **resumo** (quantos itens, valor total)
3. Clique em **"Finalizar Entrada"**
4. **CONFIRME** e pronto! ✅ Estoque atualizado!

---

## 🏷️ **COMO CADASTRAR PRODUTO NOVO**

### **QUANDO USAR:**
- Produto novo que nunca foi vendido
- Primeira vez que recebe um produto
- Código de barras não foi encontrado

### **PASSO 1: Acesse Cadastro de Produtos**
1. Menu lateral → **"Produtos"**
2. Clique em **"Adicionar Produto"**

### **PASSO 2: Informações Básicas**
1. **Nome do produto**: Digite um nome claro (ex: "Camiseta Azul M")
2. **Categoria**: Escolha o tipo (ex: Roupas, Calçados)
3. **Marca**: Escolha a marca ou adicione nova

### **PASSO 3: Código de Barras com Scanner**
1. **ATENÇÃO!** Esta é a parte mais importante! 🎯
2. Clique no campo **"Código de Barras"**
3. **ESCANEIE** o código de barras do produto
4. Sistema vai verificar se já existe:
   - ✅ **Verde**: Código novo, pode usar!
   - ⚠️ **Amarelo**: Código já existe, clique para ver qual produto
   - ❌ **Vermelho**: Código inválido, tente novamente

### **PASSO 4: Preços**
1. **Preço de Custo**: Quanto você pagou pelo produto
2. **Preço de Venda**: Quanto você vai vender
3. **O sistema calcula automaticamente sua margem de lucro!** 💰

### **PASSO 5: Salvar**
1. Clique em **"Salvar Produto"**
2. **PRONTO!** 🎉 Produto cadastrado e pronto para vender!

---

## 🔧 **CONFIGURAÇÃO DO LEITOR DE CÓDIGO DE BARRAS**

### **COMO CONECTAR:**
1. **Conecte o leitor USB** no computador
2. **Windows vai reconhecer automaticamente** (como se fosse um teclado)
3. **Teste**: Abra um bloco de notas e escaneie - deve digitar o código

### **SE NÃO FUNCIONAR:**
1. ✅ Verifique se está conectado direito
2. ✅ Tente outra porta USB
3. ✅ Reinicie o computador
4. ✅ Teste em outro programa antes

### **DICAS IMPORTANTES:**
- 📍 **Clique sempre no campo** antes de escanear
- 📍 **Espere o "bip"** do leitor antes do próximo scan
- 📍 **Mantenha distância correta** (normalmente 5-10cm)
- 📍 **Código limpo** funciona melhor

---

## ❓ **PROBLEMAS COMUNS E SOLUÇÕES**

### **🚨 "Produto não encontrado"**
**SOLUÇÃO**: O produto não está cadastrado
1. Vá em **Produtos → Adicionar Produto**
2. Cadastre o produto primeiro
3. Depois volte para a venda

### **🚨 "Scanner não funciona"**
**SOLUÇÃO**: Verificar configuração
1. Teste o scanner no bloco de notas
2. Se não digitar, problema é no scanner
3. Se digitar, clique no campo correto antes de escanear

### **🚨 "Código já existe"**
**SOLUÇÃO**: Na tela de cadastro
1. Sistema mostra qual produto já tem esse código
2. Clique em **"Visualizar"** ou **"Editar"**
3. Ou use um código diferente

### **🚨 "Estoque zerado"**
**SOLUÇÃO**: Produto sem estoque
1. Vá em **Entradas de Estoque**
2. Faça uma entrada do produto
3. Depois volta para a venda

---

## 🎯 **FLUXO COMPLETO DO SEU NEGÓCIO**

### **1️⃣ CHEGOU MERCADORIA:**
**Entradas** → Scanner produtos → Finalizar → ✅ Estoque atualizado

### **2️⃣ PRODUTO NOVO:**
**Produtos** → Cadastrar → Scanner código → Salvar → ✅ Pronto para vender

### **3️⃣ FAZER VENDA:**
**Venda Rápida** → Scanner produtos → Finalizar → ✅ Venda e estoque atualizados

### **4️⃣ CONTROLAR TUDO:**
**Dashboard** → Veja vendas, estoque, relatórios → ✅ Negócio sob controle

---

## 🏆 **DICAS DE OURO**

### **⚡ Para ser SUPER RÁPIDO:**
1. **Mantenha o scanner sempre à mão**
2. **Cadastre produtos assim que chegam**
3. **Use códigos de barras sempre que possível**
4. **Organize produtos por categoria**

### **🛡️ Para EVITAR ERROS:**
1. **Confira sempre a tela** antes de finalizar
2. **Teste scanner antes de começar o dia**
3. **Mantenha códigos limpos** e legíveis
4. **Cadastre fornecedores corretamente**

### **💰 Para MAXIMIZAR LUCRO:**
1. **Veja margem de lucro** no cadastro
2. **Controle estoque mínimo**
3. **Acompanhe relatórios** semanalmente
4. **Use dashboard** para tomar decisões

---

## 🆘 **PRECISA DE AJUDA?**

### **PRIMEIRO:**
1. ✅ Leia este manual novamente
2. ✅ Teste com calma, passo a passo
3. ✅ Verifique se scanner está funcionando

### **AINDA COM PROBLEMAS:**
1. 📧 Anote exatamente o que aconteceu
2. 📱 Tire uma foto da tela se der erro
3. 🤝 Procure suporte técnico

---

## 🎉 **PARABÉNS!**

**Você agora sabe operar o sistema SGE!**

**Lembre-se**: 
- 🚀 **Prática leva à perfeição**
- 🎯 **Scanner facilita tudo**
- 💡 **Sistema é seu aliado, não inimigo**

**BOA SORTE COM SEU NEGÓCIO!** 🏪💰

---
"""

    # Converter markdown para HTML
    html_content = markdown.markdown(
        manual_content,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    context = {
        'manual_html': html_content,
        'title': 'Manual de Operação - SGE'
    }
    
    return render(request, 'manual/manual_operacao.html', context)
