# Guia da equipe — Patch Works v2.0

Onboarding para integrantes do projeto acadêmico.

## 1. Clonar a versão principal (v2)

```bash
git clone https://github.com/gentilneto/patchworks.git
cd patchworks
# main já é a v2.0
```

Para ver a v1 antiga (somente leitura / comparação):

```bash
git checkout v1.0
git checkout main   # voltar para a atual
```

## 2. Ambiente Python

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## 3. Arquivo `.env`

```bash
copy .env.example .env
```

Edite no mínimo:

- `MYSQL_*` — usuário/senha do MySQL da aplicação (não use root no Django)  
- Origem do frete — preferir **Admin → Configuração da loja**; `STORE_CEP` no `.env` é só fallback  
- `MELHOR_ENVIO_*` — se for testar frete (cada um pode usar a própria conta sandbox)

**Nunca commite o `.env` nem o `melhorenvio_token.json`.**

## 4. MySQL

Crie o banco (WorkBench ou CLI):

```sql
CREATE DATABASE IF NOT EXISTS patchworks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'patchworks'@'localhost' IDENTIFIED BY 'patchworks123';
GRANT ALL PRIVILEGES ON patchworks.* TO 'patchworks'@'localhost';
FLUSH PRIVILEGES;
```

Depois:

```bash
python manage.py migrate
python manage.py loaddata data/fixture_inicial.json
python manage.py createsuperuser
```

As imagens já estão em `media/` no repositório.

## 5. Rodar

```bash
python manage.py runserver
```

- http://127.0.0.1:8000/  
- http://127.0.0.1:8000/admin/

## 6. Frete + túnel Cloudflare (opcional por integrante)

O callback OAuth do Melhor Envio exige **HTTPS**. Resumo no [README](../README.md#túnel-cloudflare-https-local--para-o-time):

1. `cloudflared tunnel --url http://127.0.0.1:8000`  
2. Atualizar `.env` + callback com a URL `trycloudflare.com`  
3. Autorizar em `/api/melhorenvio/autorizar/`  
4. **Fechar:** `Ctrl + C` no terminal do cloudflared (a URL deixa de funcionar)

Detalhes: `docs/MANUAL_MELHOR_ENVIO.md` e `docs/PASSO_A_PASSO_CLOUDFLARED.md`.

## 7. O que cada um deve versionar

| Pode commitar | Não commitar |
|---------------|--------------|
| Código, templates, CSS/JS | `.env` |
| `media/` (se novas fotos de demo) | `melhorenvio_token.json` |
| Docs / README | `venv/` |
| `data/fixture_inicial.json` | senhas / tokens |

## 8. Dúvidas

Índice completo: [README.md](../README.md) e [docs/README.md](README.md).
