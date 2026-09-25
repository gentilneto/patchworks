# Manual Cloudflare Tunnel (trycloudflare) — v2.0

Instalação passo a passo: [PASSO_A_PASSO_CLOUDFLARED.md](PASSO_A_PASSO_CLOUDFLARED.md).

## 1. Para que serviu / serve

O Melhor Envio **não aceita** callback OAuth em `http://127.0.0.1` (exige **HTTPS**).

Em vez de publicar o Django na Vercel, usamos um **túnel** no PC do desenvolvedor:

```
Internet (HTTPS)  →  Cloudflare  →  seu PC (http://127.0.0.1:8000)
```

Ferramenta: **cloudflared** (Cloudflare Tunnel “quick tunnel”).

Comando usado:

```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8000
```

Isso gera uma URL temporária do tipo:

```
https://algo-aleatorio.trycloudflare.com
```

Essa URL foi usada como:

- Site / URL de testes do app Melhor Envio  
- `MELHOR_ENVIO_REDIRECT_URI=.../api/melhorenvio/callback/`  
- Host em `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS`

---

## 2. Tem custo?

| Uso | Custo |
|-----|--------|
| Quick tunnel `*.trycloudflare.com` (sem conta) | **Gratuito** |
| Túnel nomeado / produção com conta Cloudflare | Planos pagos conforme o produto |

Para o nosso caso acadêmico/sandbox: **sem custo**.

Limitações do quick tunnel:

- Sem garantia de uptime  
- URL muda se você reiniciar o `cloudflared`  
- Só funciona enquanto o PC e o Django estão ligados  

---

## 3. Se eu desligar a máquina, o site cai?

**Sim.**

Hoje o site roda **na sua máquina**:

| Componente | Onde roda |
|------------|-----------|
| Django (`runserver`) | Seu PC |
| MySQL | Seu PC |
| Túnel Cloudflare | Seu PC (encaminha para o Django) |

Ao desligar o PC (ou fechar os processos):

- http://127.0.0.1:8000 para  
- a URL `trycloudflare.com` para de responder  
- a cotação/OAuth públicos deixam de funcionar até subir tudo de novo  

Para o site ficar no ar 24h, é preciso **hospedagem contínua** (servidor/cloud), não só túnel.

---

## 4. Como usar de novo

1. Suba MySQL + `python manage.py runserver`  
2. Suba o túnel com o comando da seção 1  
3. Copie a **nova** URL HTTPS exibida no terminal  
4. Atualize no `.env`:

```env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,NOVA-URL-SEM-HTTPS
DJANGO_CSRF_TRUSTED_ORIGINS=https://NOVA-URL
MELHOR_ENVIO_REDIRECT_URI=https://NOVA-URL/api/melhorenvio/callback/
```

5. Atualize a mesma URL de callback no painel Melhor Envio (Área Dev → editar app)  
6. Reinicie o Django para reler o `.env`  
7. Se precisar de token novo: abra `/api/melhorenvio/autorizar/`

---

## 5. Alternativa futura

Publicar o Django em Render/Railway/VPS com domínio HTTPS próprio.  
Aí o túnel deixa de ser necessário para OAuth.
