from django.contrib import admin
#iato painel adm do django

from .models import Avaliacao, Produto, ProdutoImagem
#importa os dois models do app core

class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ProdutoImagemInline]

admin.site.register(Avaliacao)
#faz a tabela avaliacao aparecer no admin

admin.site.register(Produto, ProdutoAdmin)
#faz a tabela produto aparecer no admin