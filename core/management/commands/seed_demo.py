from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Avaliacao, Categoria, Produto, ProdutoImagem


class Command(BaseCommand):
    help = 'Carrega o catálogo de demonstração somente em um banco sem catálogo.'

    def handle(self, *args, **options):
        catalog_models = (Categoria, Produto, ProdutoImagem, Avaliacao)
        if any(model.objects.exists() for model in catalog_models):
            self.stdout.write('Catálogo já existente; nenhum dado foi alterado.')
            return

        fixture = Path(__file__).resolve().parents[3] / 'data' / 'fixture_demo.json'
        with transaction.atomic():
            call_command('loaddata', str(fixture), verbosity=0)

        self.stdout.write(self.style.SUCCESS('Catálogo de demonstração carregado.'))
