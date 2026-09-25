from django.contrib import admin
# importa o painel administrativo do Django
from django.utils.html import format_html
# permite usar HTML dentro do admin (ex: mostrar imagem)
from .models import Avaliacao, ConfiguracaoLoja, Produto, ProdutoImagem, Categoria
# importa os models do app core


@admin.register(ConfiguracaoLoja)
class ConfiguracaoLojaAdmin(admin.ModelAdmin):
    list_display = ('cep', 'endereco', 'atualizado_em')
    fields = ('cep', 'endereco', 'atualizado_em')
    readonly_fields = ('atualizado_em',)

    def has_add_permission(self, request):
        return not ConfiguracaoLoja.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        ConfiguracaoLoja.get_solo()
        return super().changelist_view(request, extra_context=extra_context)


class ProdutoImagemInline(admin.TabularInline):
    # permite adicionar imagens extras dentro do produto no admin
    model = ProdutoImagem
    extra = 1  
    # quantidade de campos extras vazios
    verbose_name = "Imagem adicional"
    verbose_name_plural = "Imagens adicionais"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # configura como a categoria aparece no admin
    list_display = ('nome',)  
    #colunas exibidas
    search_fields = ('nome',)  
    #campo de busca

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # configura a tabela de produtos no admin

    list_display = (
        # miniatura da imagem
        'preview_imagem',  
        'nome',
        'categoria',
        'codigo',
        'preco',
        'tem_desconto',
        'preco_desconto',
        'publicado_em',
    )

    search_fields = ('nome', 'codigo')
    # permite buscar por nome e código

    list_filter = ('publicado_em', 'categoria', 'tem_desconto')
    # filtros laterais

    inlines = [ProdutoImagemInline]
    # permite adicionar imagens extras dentro do produto

    fieldsets = (
        ('Informações básicas', {
            'fields': (
                'nome',
                'categoria',
                'codigo',
                'descricao',
                'imagem',
            )
        }),

        ('Preço', {
            'fields': (
                'preco',
                'tem_desconto',
                'preco_desconto',
            )
        }),

        ('Contato e detalhes', {
            'fields': (
                'whatsapp_numero',
                'medidas',
                'peso',
                'quantidade_minima',
                'prazo_dias_uteis',
                'publicado_em',
            )
        }),

        ('Frete (Melhor Envio)', {
            'fields': (
                'altura_cm',
                'largura_cm',
                'comprimento_cm',
                'peso_kg',
            ),
            'description': 'Dimensões da embalagem em cm e peso em kg para cotação de frete.',
        }),
    )
    # organiza o formulário do admin em blocos (mais profissional)

    def preview_imagem(self, obj):
        # função para mostrar a imagem dentro da tabela do admin
        if obj.imagem:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px;" />',
                obj.imagem.url
            )
        return "Sem imagem"

    preview_imagem.short_description = "Imagem"
    # nome da coluna no admin


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    # configuração do admin para avaliações

    list_display = ('preview_imagem', 'titulo', 'produto', 'criado_em')
    search_fields = ('titulo', 'descricao')
    list_filter = ('criado_em', 'produto')

    fields = (
        'produto',
        'titulo',
        'descricao',
        'imagem',
        'link',
    )

    def preview_imagem(self, obj):
        # mostra miniatura da imagem da avaliação
        if obj.imagem:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px;" />',
                obj.imagem.url
            )
        return "Sem imagem"

    preview_imagem.short_description = "Imagem"

#admin.site.register(Avaliacao)
#faz a tabela avaliacao aparecer no admin

#admin.site.register(Produto, ProdutoAdmin)
#faz a tabela produto aparecer no admin