# Manual de rotas e APIs (v2.0)

Referência das URLs do app `core` (`core/urls.py`).

Base local: `http://127.0.0.1:8000`

Branch principal do código: `main` (v2.0).


---

## 1. Páginas (HTML)

| Método | Rota | Nome | View | Descrição |
|--------|------|------|------|-----------|
| GET | `/` | `home` | `home` | Página inicial |
| GET | `/produtos/` | `produtos` | `produtos` | Catálogo + modal + cotação |
| GET | `/avaliacoes/` | `avaliacoes` | `avaliacoes` | Lista de avaliações |
| GET | `/contato/` | `contato` | `contato` | Contato / endereço |
| GET | `/admin/` | — | Django Admin | Gestão (login necessário) |

### Query params em `/produtos/`

| Param | Exemplo | Efeito |
|-------|---------|--------|
| `busca` | `?busca=brinco` | Filtra por nome |
| `categoria` | `?categoria=1` | Filtra por ID da categoria |

---

## 2. APIs JSON

### 2.1 Consultar CEP (ViaCEP)

```
GET /api/cep/?cep=01310-100
```

**Resposta OK (200):**

```json
{
  "ok": true,
  "endereco": {
    "cep": "01310-100",
    "logradouro": "Avenida Paulista",
    "bairro": "Bela Vista",
    "localidade": "São Paulo",
    "uf": "SP"
  }
}
```

**Erros comuns:** `400` CEP inválido · `404` CEP não encontrado · `502` falha ViaCEP

---

### 2.2 Cotar frete (Melhor Envio)

```
POST /api/frete/cotar/
Content-Type: application/json
X-CSRFToken: <cookie csrftoken>
```

**Body:**

```json
{
  "produto_id": 1,
  "cep": "01310100",
  "quantidade": 100
}
```

**Fluxo interno:**

1. Valida quantidade (respeita compra mínima do produto)  
2. Consulta ViaCEP no CEP destino  
3. Monta `products[]` com dimensões/peso/seguro  
4. Chama Melhor Envio `POST /api/v2/me/shipment/calculate`  
5. Devolve opções com `custom_price` / prazo  

**Resposta OK (200):**

```json
{
  "ok": true,
  "endereco": { "...": "..." },
  "origem_cep": "07094000",
  "produto": { "id": 1, "nome": "...", "quantidade": 100, "dimensoes": {} },
  "opcoes": [
    {
      "company": "Jadlog",
      "name": ".Package",
      "price": "69.48",
      "delivery_time": 8
    }
  ]
}
```

**Erros comuns:**

| Status | Motivo |
|--------|--------|
| 400 | CEP/quantidade inválidos ou abaixo do mínimo |
| 503 | Token Melhor Envio ausente |
| 401/502 | Token inválido ou falha na API externa |

**Quem chama:** `core/static/core/js/produtos.js` (botão “Calcular” no modal).

---

### 2.3 OAuth Melhor Envio

| Método | Rota | Função |
|--------|------|--------|
| GET | `/api/melhorenvio/autorizar/` | Redireciona para o OAuth sandbox/produção |
| GET | `/api/melhorenvio/callback/` | Recebe `?code=` e grava `melhorenvio_token.json` |

Detalhes: [MANUAL_MELHOR_ENVIO.md](MANUAL_MELHOR_ENVIO.md).

---

## 3. Serviços Python (não são URLs)

| Arquivo | Responsabilidade |
|---------|------------------|
| `core/services/viacep.py` | `consultar_cep()` |
| `core/services/melhor_envio.py` | OAuth, token, `calcular_frete_produtos()` |

---

## 4. Testes manuais sugeridos (PowerShell / curl)

```powershell
# CEP
curl.exe "http://127.0.0.1:8000/api/cep/?cep=07094000"

# Página produtos (gera cookie CSRF no navegador)
# Depois use o DevTools > Network para inspecionar POST /api/frete/cotar/
```

Ou abra `/produtos/`, clique num produto, informe CEP e quantidade.

---

## 5. Quando adicionar uma nova API

1. Criar função em `core/views.py`  
2. Registrar em `core/urls.py`  
3. Documentar neste manual (método, body, erros)  
4. Se precisar de segredo, usar `.env` via `settings.py`  
5. Testar com CSRF (POST) ou GET conforme o caso  
