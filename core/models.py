from django.db import models  # importa o módulo de modelos do Django (ORM)
from urllib.parse import quote
# Transforma a mensagem em formato válido para URL do zap
import re
# limpa o numero removendo - ( ) espaços etc


class Categoria(models.Model):
    # para guardar o nome da categoria
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Produto(models.Model):
    # cria a tabela de produtos no banco

    nome = models.CharField(max_length=150)
    # nome do produto

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos'
    )
    # relação com a categoria

    codigo = models.CharField(max_length=50, unique=True)
    # SKU do produto

    descricao = models.TextField()
    # descrição detalhada

    preco = models.DecimalField(max_digits=8, decimal_places=2)
    # preço original do produto

    tem_desconto = models.BooleanField("Tem desconto?", default=False)
    # marca se o produto tem desconto

    preco_desconto = models.DecimalField(
        "Preço com desconto",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    # preço promocional / no pix

    imagem = models.ImageField(upload_to='produtos/')
    # imagem principal do produto

    medidas = models.CharField(max_length=100, blank=True)
    # medidas exibidas (texto livre)

    peso = models.CharField(max_length=50, blank=True)
    # peso exibido (texto livre)

    # Dimensões usadas na cotação Melhor Envio (cm / kg)
    altura_cm = models.PositiveIntegerField(
        "Altura (cm)",
        null=True,
        blank=True,
        help_text="Usado na cotação de frete (Melhor Envio)",
    )
    largura_cm = models.PositiveIntegerField(
        "Largura (cm)",
        null=True,
        blank=True,
        help_text="Usado na cotação de frete (Melhor Envio)",
    )
    comprimento_cm = models.PositiveIntegerField(
        "Comprimento (cm)",
        null=True,
        blank=True,
        help_text="Usado na cotação de frete (Melhor Envio)",
    )
    peso_kg = models.DecimalField(
        "Peso (kg)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Usado na cotação de frete (Melhor Envio)",
    )

    quantidade_minima = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Exemplo: 100"
    )
    # quantidade mínima do pedido
    prazo_dias_uteis = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Exemplo: 8"
    )
    # prazo de produção/entrega em dias úteis

    publicado_em = models.DateField(null=True, blank=True)
    # data de publicação

    whatsapp_numero = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Digite no formato: 5511999999999 (sem espaço ou hífen)"
    )
    # número que será usado para montar o link do WhatsApp

    criado_em = models.DateTimeField(auto_now_add=True)
    # salva automaticamente a data e hora quando o produto for criado

    def __str__(self):
        return self.nome
        # mostra o nome do produto

    @property
    def whatsapp_link(self):
        if not self.whatsapp_numero:
            return "#"

        numero = re.sub(r'\D', '', self.whatsapp_numero)
        mensagem = f"Olá, tenho interesse no produto {self.nome}. Código: {self.codigo}"
        return f"https://wa.me/{numero}?text={quote(mensagem)}"

    @property
    def porcentagem_desconto(self):
        if self.tem_desconto and self.preco_desconto:
            return int(((self.preco - self.preco_desconto) / self.preco) * 100)
        return 0

    @property
    def preco_seguro(self):
        """Valor unitário para insurance_value na cotação."""
        if self.tem_desconto and self.preco_desconto is not None:
            return self.preco_desconto
        return self.preco

    def dimensoes_unidade(self):
        """
        Dimensões/peso UNITÁRIOS para a cotação Melhor Envio (products[]).
        Não aplica mínimos de embalagem por peça — a API empacota a quantidade.
        """
        height = max(int(self.altura_cm or 1), 1)
        width = max(int(self.largura_cm or 1), 1)
        length = max(int(self.comprimento_cm or 1), 1)
        weight = float(self.peso_kg or 0)
        if weight <= 0:
            weight = 0.001
        return {
            'height': height,
            'width': width,
            'length': length,
            'weight': round(weight, 3),
        }

    def dimensoes_frete(self, quantidade=1):
        """
        Compatível com o fluxo antigo: retorna unidade real.
        quantidade é informativa (peso total estimado).
        """
        unidade = self.dimensoes_unidade()
        qtd = max(int(quantidade or 1), 1)
        return {
            **unidade,
            'quantity': qtd,
            'peso_total_kg': round(unidade['weight'] * qtd, 3),
        }

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"


class Avaliacao(models.Model):
    # cria uma tabela no banco chamada Avaliacao

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        null=True,
        blank=True
    )
    # cada avaliação pode pertencer a um produto

    titulo = models.CharField(max_length=150)
    # título da avaliação

    descricao = models.TextField()
    # texto longo da avaliação

    imagem = models.ImageField(upload_to='avaliacoes/')
    # salva na pasta media/avaliacoes/

    link = models.URLField()
    # link externo da avaliação

    criado_em = models.DateTimeField(auto_now_add=True)
    # data/hora automática

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"