from django.shortcuts import render
from .models import Avaliacao, Produto, Categoria
#importa os models que serão usados nas views
#from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def avaliacoes(request):
    # função chamada quando acessa /avaliacoes/
    avaliacoes = Avaliacao.objects.all().order_by('-criado_em')  
    # busca todas as avaliações do banco, ordenando da mais nova para a mais antiga
    return render(request, 'core/avaliacoes.html', {'avaliacoes': avaliacoes})  
    # envia os dados para o HTML (template)

'''
    def produtos(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    #busca todos os produtos no banco, do mais novo para o mais antigo.
    return render(request, 'core/produtos.html', {'produtos': produtos})
    #envia os produtos para template produtos.html

'''

def produtos(request):
    busca = request.GET.get('busca', '')
    categoria_id = request.GET.get('categoria', '')

    produtos = Produto.objects.all().order_by('-criado_em')

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all().order_by('nome')

    return render(request, 'core/produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
        'categoria_id': categoria_id,
    })

def contato(request):
    return render(request, 'core/contato.html')