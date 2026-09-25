# 🧵 Patch Works e Afins — Versão 2.0

Catálogo online de artesanato sob encomenda (projeto acadêmico).

**Branch principal:** `main` (= **v2.0**)  
**Versão anterior:** branch `v1.0` (SQLite / layout antigo) — preservada no GitHub.

Repositório: https://github.com/gentilneto/patchworks

---

## O que há na v2.0

- Catálogo com busca, categorias e modal de produto  
- Avaliações e página de contato  
- Identidade visual artesanal (UX/UI)  
- Banco **MySQL**  
- Cotação de frete (**Melhor Envio**) no modal  
- Origem do frete editável no **Admin** (CEP + endereço)  
- Validação de CEP (**ViaCEP**)  
- Admin Django  
- Manuais em `docs/`  
- Dados de exemplo em `data/fixture_inicial.json`  
- Mídias em `media/`

---

## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3 + Django 6 |
| Banco | MySQL 8 |
| Front | HTML / CSS / JS |
| Frete | Melhor Envio API (sandbox/produção) |
| CEP | ViaCEP |

---

## Branches

| Branch | Conteúdo |
|--------|----------|
| **`main`** | **v2.0 (atual / principal)** |
| `v1.0` | Versão 1.0 original (não apagada) |
| `v2.0` | Espelho da v2 (opcional; use `main`) |

```bash
# Clonar a versão atual (v2)
git clone https://github.com/gentilneto/patchworks.git
cd patchworks

# Se precisar da v1 antiga:
git checkout v1.0
```

---

## Como rodar (equipe)

### Pré-requisitos

- Python 3.12+ (ou 3.14)  
- MySQL 8.x rodando localmente  
- Conta Melhor Envio **Sandbox** (para frete)

### Passos

```bash
git clone https://github.com/gentilneto/patchworks.git
cd patchworks

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt

# Configurar ambiente
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
# Edite .env (MySQL + Melhor Envio)
```

### Banco MySQL

1. Crie o banco e o usuário (ajuste senha se quiser):

```sql
CREATE DATABASE IF NOT EXISTS patchworks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'patchworks'@'localhost' IDENTIFIED BY 'patchworks123';
GRANT ALL PRIVILEGES ON patchworks.* TO 'patchworks'@'localhost';
FLUSH PRIVILEGES;
```

2. Migre e carregue os dados de exemplo:

```bash
python manage.py migrate
python manage.py loaddata data/fixture_inicial.json
python manage.py createsuperuser
```

### Servidor

```bash
python manage.py runserver
```

- Site: http://127.0.0.1:8000/  
- Admin: http://127.0.0.1:8000/admin/

### Melhor Envio (cotação)

1. Cadastre um app em **Integrações → Área Dev.** (sandbox)  
2. Preencha `MELHOR_ENVIO_CLIENT_ID`, `CLIENT_SECRET` e `REDIRECT_URI` no `.env`  
3. Callback precisa de **HTTPS** (use Cloudflare Tunnel — ver `docs/PASSO_A_PASSO_CLOUDFLARED.md`)  
4. Autorize: http://127.0.0.1:8000/api/melhorenvio/autorizar/  

Detalhes: `docs/MANUAL_MELHOR_ENVIO.md`

---

## Estrutura

```
patchworks/
├── core/                 # App Django (models, views, templates, static, services)
├── patchworks/           # Settings / URLs do projeto
├── media/                # Imagens de produtos e avaliações
├── data/                 # Fixture Django para a equipe
├── docs/                 # Manuais de manutenção
├── .env.example          # Modelo de configuração (copie para .env)
├── requirements.txt
├── breagnote.md          # Pitch do produto
└── manage.py
```

---

## Manuais

| Arquivo | Assunto |
|---------|---------|
| [docs/README.md](docs/README.md) | Índice |
| [docs/MANUAL_MANUTENCAO.md](docs/MANUAL_MANUTENCAO.md) | Manutenção / setup |
| [docs/MANUAL_API.md](docs/MANUAL_API.md) | Rotas e APIs |
| [docs/MANUAL_MELHOR_ENVIO.md](docs/MANUAL_MELHOR_ENVIO.md) | Frete / OAuth |
| [docs/PASSO_A_PASSO_CLOUDFLARED.md](docs/PASSO_A_PASSO_CLOUDFLARED.md) | Túnel HTTPS |
| [docs/MANUAL_CLOUDFLARE.md](docs/MANUAL_CLOUDFLARE.md) | Conceito do túnel |
| [docs/HIGIENIZACAO.md](docs/HIGIENIZACAO.md) | Limpeza do projeto |
| [docs/GUIA_EQUIPE.md](docs/GUIA_EQUIPE.md) | Onboarding dos integrantes |

---

## Segurança (importante para o time)

**Não versionamos** (e não devem ir para o Git):

- `.env` (senhas / tokens reais)  
- `melhorenvio_token.json`  
- `venv/`  

Cada integrante usa o próprio `.env` a partir do `.env.example` e gera o próprio token Melhor Envio.

---

## Bibliografia

1. MENEZES, Nilo. *Introdução à Programação com Python*. 4. ed. Novatec, 2024.  
2. SILBERSCHATZ et al. *Sistemas de Banco de Dados*. 6. ed. Elsevier, 2012.  
3. GAMMA et al. *Padrões de Projeto*. Bookman, 2000.  
4. Django Software Foundation. Documentação oficial — https://docs.djangoproject.com/pt-br/  
5. MDN Web Docs — https://developer.mozilla.org/pt-BR/  
6. Melhor Envio — https://docs.melhorenvio.com.br/  

---

⚠️ Mídias e fixture são para fins acadêmicos e colaboração em equipe.
