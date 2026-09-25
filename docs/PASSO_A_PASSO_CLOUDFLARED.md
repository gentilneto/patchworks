# Passo a passo — instalar e usar o cloudflared (v2.0)

O `cloudflared` cria um **túnel HTTPS** temporário da internet até o Django no seu PC  
(`https://….trycloudflare.com` → `http://127.0.0.1:8000`).

Útil para o Melhor Envio (callback OAuth exige HTTPS). Ver também [MANUAL_CLOUDFLARE.md](MANUAL_CLOUDFLARE.md).

---

## Opção A — Windows com winget (recomendada)

### 1. Abrir o PowerShell

Menu Iniciar → digite `PowerShell` → Enter.

### 2. Instalar

```powershell
winget install Cloudflare.cloudflared --accept-package-agreements --accept-source-agreements
```

### 3. Fechar e abrir o PowerShell de novo

Para o PATH atualizar.

### 4. Conferir se instalou

```powershell
cloudflared --version
```

Se não achar o comando, use o caminho completo:

```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" --version
```

---

## Opção B — Download manual

1. Acesse: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/  
2. Baixe o instalador **Windows (amd64)**  
3. Instale o `.msi`  
4. Teste com `cloudflared --version`

---

## Como usar no Patch Works

### Pré-requisitos (em outros terminais)

1. MySQL rodando  
2. Django:

```powershell
cd C:\Projetos\patchworks
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Subir o túnel

**Novo** PowerShell:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Ou:

```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8000
```

### Copiar a URL

No terminal aparece algo como:

```
https://nome-aleatorio.trycloudflare.com
```

Abra essa URL no navegador — deve mostrar o site.

### Alinhar o projeto (se a URL mudou)

No `.env`:

```env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,nome-aleatorio.trycloudflare.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://nome-aleatorio.trycloudflare.com
MELHOR_ENVIO_REDIRECT_URI=https://nome-aleatorio.trycloudflare.com/api/melhorenvio/callback/
```

Atualize o **mesmo** callback no Melhor Envio (Área Dev → editar app).  
Reinicie o `runserver`.

---

## Parar / fechar o túnel

Quando não precisar mais do HTTPS público:

1. Vá no terminal onde o `cloudflared` está rodando.  
2. Pressione **`Ctrl + C`** — o túnel encerra na hora.  
3. A URL `https://….trycloudflare.com` **para de funcionar**.  
4. O Django local (`runserver`) pode continuar; o site fica só em http://127.0.0.1:8000/.  
5. Se quiser parar o site também, no terminal do Django use **`Ctrl + C`**.

Não é necessário desinstalar o `cloudflared`. Na próxima autorização OAuth, abra o túnel de novo (a URL muda → atualize `.env` e o app Melhor Envio).

---

## Custos e limites

| Item | Detalhe |
|------|---------|
| Preço (quick tunnel) | **Grátis** |
| Conta Cloudflare | Não obrigatória nesse modo |
| Se desligar o PC | Site/túnel **caem** |
| URL | Muda ao reiniciar o túnel |

Mais detalhes: [MANUAL_CLOUDFLARE.md](MANUAL_CLOUDFLARE.md)
