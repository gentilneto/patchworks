from django.shortcuts import render
from .models import Avaliacao
#from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def avaliacoes(request):
    # função chamada quando acessa /avaliacoes/
    avaliacoes = Avaliacao.objects.all().order_by('-criado_em')  
    # busca todas as avaliações do banco, ordenando da mais nova para a mais antiga
    return render(request, 'core/avaliacoes.html', {'avaliacoes': avaliacoes})  
    # envia os dados para o HTML (template)

def contato(request):
    return render(request, 'core/contato.html')