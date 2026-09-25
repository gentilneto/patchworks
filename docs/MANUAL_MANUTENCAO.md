# Manual de manutenção — Patch Works e Afins

Guia prático para manter o site no dia a dia (desenvolvimento local).

---

## 1. O que é este projeto

Catálogo online Django da loja **Patch Works e Afins**:

- Páginas: Início, Produtos, Avaliações, Contato
- Admin Django para produtos e avaliações
- Banco **MySQL**
- Cotação de frete via **Melhor Envio** + validação de CEP via **ViaCEP**

Estrutura principal:

```
patchworks/
├── manage.py
├── .env                 # segredos (não versionar)
├── melhorenvio_token.json  # token OAuth (não versionar)
├── requirements.txt
├── core/                # app principal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/        # Melhor Envio + ViaCEP
│   ├── templates/core/
│   └── static/core/
└── patchworks/
    └── settings.py
```

---

## 2. Como subir o ambiente (checklist)

### 2.1 Uma vez (já feito na máquina atual)

1. Python + venv em `venv/`
2. `pip install -r requirements.txt`
3. MySQL 8.4 instalado, banco `patchworks`, usuário `patchworks`
4. Arquivo `.env` preenchido (copie de `.env.example`)

### 2.2 Toda vez que reiniciar o PC

O site **não** fica no ar sozinho. Precisa:

```powershell
# 1) MySQL (se não estiver como serviço Windows)
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" --defaults-file="C:\ProgramData\MySQL\MySQL Server 8.4\my.ini"

# 2) Django
cd C:\Projetos\patchworks
.\venv\Scripts\Activate.ps1
python manage.py runserver

# 3) (Opcional) Túnel HTTPS — só se precisar de callback OAuth público
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8000
```

Acesso local: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/

---

## 3. Banco de dados (MySQL)

| Item | Valor padrão |
|------|----------------|
| Engine | `django.db.backends.mysql` |
| Host | `127.0.0.1:3306` |
| Database | `patchworks` |
| Driver Python | PyMySQL |

**SQLite (`db.sqlite3`) não é mais usado pelo Django.**  
O arquivo antigo pode existir na pasta só como backup histórico; o `settings.py` aponta exclusivamente para MySQL.

### Comandos úteis

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py dumpdata core --indent 2 -o backup_core.json
```

### Cadastro de conteúdo

Use o Admin:

- **Categorias / Produtos / Imagens** — catálogo e cotação (preencha `altura_cm`, `largura_cm`, `comprimento_cm`, `peso_kg`)
- **Avaliações** — depoimentos da página pública

---

## 4. Variáveis importantes (`.env`)

| Variável | Função |
|----------|--------|
| `MYSQL_*` | Conexão MySQL |
| `STORE_CEP` | CEP de origem do frete (loja) |
| `MELHOR_ENVIO_CLIENT_ID` / `SECRET` | App OAuth |
| `MELHOR_ENVIO_REDIRECT_URI` | Callback HTTPS (túnel ou domínio) |
| `MELHOR_ENVIO_BASE_URL` | Sandbox ou produção |
| `DJANGO_ALLOWED_HOSTS` | Hosts aceitos (inclui domínio do túnel) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens HTTPS confiáveis |

Nunca commitar `.env` nem `melhorenvio_token.json`.

---

## 5. Manutenção de UI

| Pasta | Uso |
|-------|-----|
| `core/templates/core/` | HTML |
| `core/static/core/css/` | Visual (design system em `style.css`) |
| `core/static/core/js/` | Menu, reveal, modal, frete |

Após mudar CSS/JS, use Ctrl+F5 no navegador se a página parecer “antiga”.

---

## 6. Checklist rápido de saúde

- [ ] MySQL escutando na porta 3306  
- [ ] `python manage.py runserver` sem erro  
- [ ] `/` e `/produtos/` abrem  
- [ ] Admin consegue editar produto  
- [ ] Cotação de frete no modal responde (token válido)  
- [ ] Se usar túnel: URL do Cloudflare ainda bate com `MELHOR_ENVIO_REDIRECT_URI`

---

## 7. Problemas comuns

| Sintoma | O que checar |
|---------|----------------|
| Erro de conexão MySQL | `mysqld` rodando? senha no `.env`? |
| Frete 503 / sem token | `melhorenvio_token.json` existe? Reautorizar em `/api/melhorenvio/autorizar/` |
| DisallowedHost | Incluir o host do túnel em `DJANGO_ALLOWED_HOSTS` |
| CSRF no frete | Abrir `/produtos/` antes (cookie CSRF) |
| Imagens quebradas | Pasta `media/` e `DEBUG=True` (dev) |

---

## 8. Próximo passo sugerido (produção)

Para o site **não cair** ao desligar o PC: hospedar Django + MySQL em serviço contínuo (ex.: Render, Railway, VPS) e apontar domínio HTTPS. O túnel Cloudflare atual é só para desenvolvimento / OAuth sandbox.
