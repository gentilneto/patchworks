
from django.db import models  # importa o módulo de modelos do Django (ORM)

class Avaliacao(models.Model):  # cria uma tabela no banco chamada Avaliacao

    titulo = models.CharField(max_length=150)  
    # campo de texto curto (até 150 caracteres)

    descricao = models.TextField()   # campo de texto longo (sem limite prático)

    imagem = models.ImageField(upload_to='avaliacoes/')   # campo para upload de imagem (salva na pasta media/avaliacoes/)
    link = models.URLField()  
    # campo para armazenar URLs (links)

    criado_em = models.DateTimeField(auto_now_add=True)  
    # salva automaticamente a data/hora quando o registro é criado

    def __str__(self):    # define como o objeto aparece no admin (nome amigável)
        return self.titulo  
        # retorna o título como representação do objeto

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"