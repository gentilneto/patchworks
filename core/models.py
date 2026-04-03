
from django.db import models  # importa o módulo de modelos do Django (ORM)

class Produto(models.Model): #cria a tabela de produtos no banco
    nome = models.CharField(max_length=150)
    #nome do produto
    codigo = models.CharField(max_length=50, unique=True)
    #SKU do produto
    descricao = models.TextField()
    #descrição detalhada
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    #preço do produto
    imagem = models.ImageField(upload_to='produtos/')
    #imagem principal do produto
    whatsapp_link = models.URLField()
    #Link para contato no whats
    medidas = models.CharField(max_length=100, blank=True)
    # medidas do produto, por exemplo: 0.1 x 0.08 x 0.01 cm
    peso = models.CharField(max_length=50, blank=True)
    #peso do produto
    publicado_em = models.DateField(null=True, blank=True)
    #data de publicação
    criado_em = models.DateTimeField(auto_now_add=True)
    ##salva automaticamente a data e hora quando o produto for criado

    def __str__(self):
        return self.nome
        #nostra o nome do produto

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


class Avaliacao(models.Model):  # cria uma tabela no banco chamada Avaliacao

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        null=True,
        blank=True
    )

    #relacao com rodutos:
    #cada avaliacao pode pertencer a um produto
    #um produto pode ter varias avaliacoes
    #se o produto fo apagado, as avaliacoes relacionadas serão apagadas

    titulo = models.CharField(max_length=150)  
    # campo de texto curto aaaaté 150 caracteres para titulo da avaliacao

    descricao = models.TextField()   
    # campo de texto longo (sem limite prático)

    imagem = models.ImageField(upload_to='avaliacoes/')   # campo para upload de imagem (salva na pasta media/avaliacoes/)
    link = models.URLField()  
    # campo para armazenar URLs links

    criado_em = models.DateTimeField(auto_now_add=True)  
    # salva automaticamente a data e hora quando o registro é criado

    def __str__(self):    # define como o objeto aparece no admin (nome amigável)
        return self.titulo  
        # retorna o título como representação do objeto

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

