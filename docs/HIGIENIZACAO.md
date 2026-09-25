# Higienização do projeto (varredura)

Data da limpeza: 2026-09-25

## Removido com segurança

| Item | Motivo |
|------|--------|
| `db.sqlite3` | Django usa MySQL; SQLite legado |
| `data_sqlite_backup.json` | Dump da migração SQLite→MySQL (dados já no MySQL) |
| `__pycache__/` (fora do venv) | Cache Python regenerável |
| `media/brincos/` | Pasta solta; imagens idênticas às de `media/produtos/` e **não** referenciadas no banco |
| `media/produtos/*_x5DbGzi.jpg`, `*_JiGQjY7.jpg`, `*_yXyaIZD.jpg` | Duplicatas de upload Django; **não** estão no MySQL |
| `core/static/core/avaliacoes/` | Cópia das fotos; o site usa `media/avaliacoes/` via `ImageField` |
| Comentário morto em `patchworks/urls.py` | Código antigo comentado |

## Mantido de propósito

| Item | Motivo |
|------|--------|
| `.env` | Segredos locais |
| `melhorenvio_token.json` | Token OAuth ativo |
| `venv/` | Ambiente Python |
| `media/produtos/*` e `media/avaliacoes/*` usados no MySQL | Conteúdo real do catálogo |
| `core/static/core/logo.png`, `img/fundo.png`, CSS/JS | Identidade visual |
| `docs/`, `breagnote.md`, `README.md` | Documentação |

## Não apagar sem planejar

- `venv/` — apagar só se for recriar (`python -m venv venv` + `pip install -r requirements.txt`)
- `melhorenvio_token.json` — sem ele a cotação falha até reautorizar
- Qualquer arquivo listado em `Produto.imagem` / `ProdutoImagem` / `Avaliacao.imagem` no Admin

## Conferência pós-limpeza sugerida

```powershell
cd C:\Projetos\patchworks
.\venv\Scripts\Activate.ps1
python manage.py check
python manage.py runserver
```

Abrir `/`, `/produtos/`, `/avaliacoes/` e um modal de produto.
