# Manual Melhor Envio — OAuth e cotação

## 1. Conceito importante

A **senha da conta** Melhor Envio **não** autentica a API.

A API exige `Authorization: Bearer <access_token>` obtido por **OAuth 2.0** após criar um aplicativo em:

**Integrações → Área Dev. → Cadastrar Aplicativo**

Documentação: https://docs.melhorenvio.com.br/reference/fluxo-de-autorização  
Cotação: https://docs.melhorenvio.com.br/reference/calculo-de-fretes-por-produtos

---

## 2. Dados do app (sandbox)

No `.env`:

```env
MELHOR_ENVIO_BASE_URL=https://sandbox.melhorenvio.com.br
MELHOR_ENVIO_CLIENT_ID=...
MELHOR_ENVIO_CLIENT_SECRET=...
MELHOR_ENVIO_REDIRECT_URI=https://SEU-DOMINIO-HTTPS/api/melhorenvio/callback/
MELHOR_ENVIO_USER_AGENT=Patch Works e Afins (seu-email@exemplo.com)
```

O callback **deve ser HTTPS** e idêntico ao cadastrado no painel.

---

## 3. Gerar / renovar o token

1. Suba o Django (`runserver`)  
2. Se o callback for público via túnel, suba o Cloudflare Tunnel e alinhe `REDIRECT_URI` + `ALLOWED_HOSTS`  
3. No navegador (já logado no sandbox):

```
http://127.0.0.1:8000/api/melhorenvio/autorizar/
```

(ou a URL do túnel + `/api/melhorenvio/autorizar/`)

4. Clique **AUTORIZAR** no Melhor Envio  
5. O callback grava `melhorenvio_token.json` na raiz do projeto  

Validade típica: `access_token` ~30 dias · `refresh_token` ~45 dias.

Quando a cotação voltar `Unauthenticated`, refaça a autorização (ou implemente refresh automático no futuro).

---

## 4. Cotação no produto

No Admin, cada produto precisa de:

- `altura_cm`, `largura_cm`, `comprimento_cm`, `peso_kg`  
- preço (seguro do frete usa preço/PIX)  
- `quantidade_minima` (se houver)

O sistema aplica mínimos de embalagem se as medidas forem muito pequenas.

Origem do frete: `STORE_CEP` (ex.: Guarulhos `07094-000`).

---

## 5. Arquivos sensíveis

| Arquivo | Conteúdo |
|---------|----------|
| `.env` | Client ID / Secret |
| `melhorenvio_token.json` | access_token / refresh_token |

Não versionar no Git (já listados no `.gitignore`).

---

## 6. Sandbox vs produção

| | Sandbox | Produção |
|--|---------|----------|
| URL base | `https://sandbox.melhorenvio.com.br` | `https://melhorenvio.com.br` |
| Conta / app | Separados | Separados |
| Uso | Testes | Envios reais |

Trocar de ambiente = novo app + novo token + atualizar `.env`.
