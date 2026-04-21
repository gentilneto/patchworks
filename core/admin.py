from django.contrib import admin
#iato painel adm do django

from django.utils.html import format_html
#permite criar op html segudo dentro do admin
from .models import Avaliacao, Produto, ProdutoImagem
#importa os dois models do app core

class ProdutoImagemInline(admin.TabularInline):
    #imagens adicionais dentro do produto
    model = ProdutoImagem
    extra = 1
    verbose_name = "Imagem adicional"
    verbose_name_plural = "Imagens adicionais"


#class ProdutoAdmin(admin.ModelAdmin):
#    inlines = [ProdutoImagemInline]

@admin.register(Produto)
#registra o modelo produto com configuração personalizada
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('preview_imagem','nome', 'codigo', 'preco', 'publicado_em')
    search_fields = ('nome', 'codigo')
    list_filter = ('publicado_em',)
    inlines = [ProdutoImagemInline]

    fields = (
        'nome',
        'codigo',
        'descricao',
        'preco',
        'imagem',
        'whatsapp_numero',
        'medidas',
        'peso',
        'publicado_em',
    )

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px;" />', obj.imagem.url)
        return "Sem imagem"
    preview_imagem.short_descrption = "Imagem"

@admin.register(Avaliacao)
#registra o modelo produto com configuração personalizada
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('preview_imagem','titulo', 'produto', 'criado_em')
    search_fields = ('titulo', 'descricao')
    #permite busca por titulo e descrição
    list_filter = ('criado_em', 'produto')
    #filtro por data e produto

    fields = (
        'produto',
        'titulo',
        'descricao',
        'imagem',
        'link',
    )

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px;" />', obj.imagem.url)
        return "Sem imagem"

    preview_imagem.short_description = "Imagem"


#admin.site.register(Avaliacao)
#faz a tabela avaliacao aparecer no admin

#admin.site.register(Produto, ProdutoAdmin)
#faz a tabela produto aparecer no admin