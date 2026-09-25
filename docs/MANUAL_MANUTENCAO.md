# Manual de manutenção — Patch Works e Afins (v2.0)

Guia prático para manter o site (desenvolvimento local / equipe acadêmica).

**Repositório:** https://github.com/gentilneto/patchworks  
**Branch principal:** `main` (v2.0) · **Arquivo v1:** branch `v1.0`

---

## 1. O que é este projeto

Catálogo Django da loja **Patch Works e Afins**:

- Páginas: Início, Produtos, Avaliações, Contato  
- Admin para produtos e avaliações  
- Banco **MySQL**  
- Cotação **Melhor Envio** + CEP **ViaCEP**

```
patchworks/
├── manage.py
├── .env.example          # modelo — copie para .env
├── data/fixture_inicial.json
├── requirements.txt
├── core/
├── docs/
├── media/
└── patchworks/settings.py
```

---

## 2. Setup completo (nova máquina)

Ver também [GUIA_EQUIPE.md](GUIA_EQUIPE.md).

```powershell
git clone https://github.com/gentilneto/patchworks.git
cd patchworks
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Editar .env (MySQL)

# MySQL: criar database/user (ver GUIA_EQUIPE)
python manage.py migrate
python manage.py loaddata data/fixture_inicial.json
python manage.py createsuperuser
python manage.py runserver
```

---

## 3. Banco MySQL

| Item | Padrão sugerido |
|------|-----------------|
| Engine | `django.db.backends.mysql` |
| Host | `127.0.0.1:3306` |
| Database / user | `patchworks` |
| Driver | PyMySQL |

**SQLite não é mais usado.** A v1 (com SQLite) ficou na branch `v1.0`.

### Comandos úteis

```powershell
python manage.py migrate
python manage.py dumpdata core auth.User --indent 2 -o data/backup_local.json
python manage.py loaddata data/fixture_inicial.json
```

---

## 4. Variáveis (`.env`)

Copie de `.env.example`. Principais:

| Variável | Função |
|----------|--------|
| `MYSQL_*` | Conexão MySQL |
| `STORE_CEP` | Origem do frete |
| `MELHOR_ENVIO_CLIENT_ID` / `SECRET` | App OAuth |
| `MELHOR_ENVIO_REDIRECT_URI` | Callback HTTPS |
| `DJANGO_ALLOWED_HOSTS` | Hosts (túnel Cloudflare etc.) |

Não versionar: `.env`, `melhorenvio_token.json`, `venv/`.

---

## 5. Checklist de saúde

- [ ] MySQL na porta 3306  
- [ ] `runserver` sem erro  
- [ ] `/` e `/produtos/` abrem  
- [ ] Imagens do catálogo aparecem  
- [ ] Cotação (se token configurado)  

---

## 6. Problemas comuns

| Sintoma | Checar |
|---------|--------|
| Erro MySQL | serviço ligado? `.env`? |
| Frete 503 | token / reautorizar OAuth |
| DisallowedHost | host do túnel no `.env` |
| Sem produtos | `loaddata data/fixture_inicial.json` |

---

## 7. Produção (futuro)

Hospedar Django + MySQL (Render/Railway/VPS) com HTTPS próprio.  
O túnel Cloudflare é só para desenvolvimento / OAuth sandbox.
