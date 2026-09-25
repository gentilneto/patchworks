# Patch Works e Afins — Brief para o dono

## Em uma frase

A **Patch Works e Afins** é uma vitrine online de artesanato sob encomenda: o cliente conhece a marca, navega no catálogo, vê avaliações, simula o frete e fala com a loja pelo WhatsApp — sem precisar de estoque pronto nem de um e-commerce completo.

---

## O que a aplicação entrega

| Para o cliente | Para a loja (você) |
|----------------|--------------------|
| Página inicial com a história da marca | Painel administrativo (Django Admin) |
| Catálogo com busca e categorias | Cadastro de produtos, fotos, preços e descontos |
| Detalhes do produto (medidas, prazo, compra mínima) | Avaliações com imagem e link externo |
| **Cotação de frete em tempo real** (Melhor Envio) | Contato e canal WhatsApp por produto |
| Página de avaliações e contato | Dados seguros em banco MySQL |

Origem dos envios (cotação):  
**Av. Dr. Timóteo Penteado, 1874 — Vila Hulda, Guarulhos/SP — CEP 07094-000**

---

## Fluxo de trabalho (do visitante ao pedido)

```
1. Visitante abre o site
        ↓
2. Navega na Home (marca + história) ou vai direto ao catálogo
        ↓
3. Filtra / busca produtos → abre o detalhe (modal)
        ↓
4. Informa o CEP de destino → sistema cotiza frete via Melhor Envio
        ↓
5. Escolhe falar no WhatsApp (mensagem já montada com nome e código do produto)
        ↓
6. Atendimento humano fecha a encomenda (produção sob medida)
```

No painel admin, a loja cadastra ou atualiza produtos e avaliações; o site público atualiza automaticamente.

---

## Tecnologias e como se comunicam

```
┌─────────────┐     HTML/CSS/JS      ┌──────────────────┐
│  Navegador  │ ◄──────────────────► │  Django (Python) │
│  do cliente │   páginas + API JSON │  app "core"      │
└─────────────┘                      └────────┬─────────┘
                                              │
                         ┌────────────────────┼────────────────────┐
                         ▼                    ▼                    ▼
                  ┌─────────────┐    ┌─────────────────┐   ┌──────────────┐
                  │   MySQL     │    │  Melhor Envio   │   │  WhatsApp    │
                  │  (dados)    │    │  (cotação frete)│   │  (wa.me)     │
                  └─────────────┘    └─────────────────┘   └──────────────┘
```

### Papel de cada peça

| Tecnologia | Função | Como se comunica |
|------------|--------|------------------|
| **HTML / CSS / JS** | Interface (páginas, modal, formulário de CEP) | O navegador pede páginas ao Django; o JS chama a rota de frete em JSON |
| **Django (Python)** | Cérebro da aplicação: rotas, regras de negócio, Admin | Lê/grava no MySQL; chama a API Melhor Envio no servidor; monta links WhatsApp |
| **MySQL** | Banco de produtos, categorias, imagens e avaliações | Django ORM (SQL sob o capô) — substitui o SQLite antigo |
| **Melhor Envio (API)** | Preços e prazos de Correios/Jadlog etc. em tempo real | Django envia CEP origem/destino + dimensões/peso/valor → recebe `custom_price` e prazo |
| **WhatsApp (link)** | Canal de venda e atendimento | Link `wa.me` gerado pelo Django; o cliente abre o app de mensagens |
| **Django Admin** | Gestão da loja sem mexer em código | Mesmo Django + MySQL, interface só para quem tem login |

### Detalhe da cotação de frete

1. Cliente digita o CEP no modal do produto.  
2. O navegador envia `produto + CEP + quantidade` para o Django.  
3. O Django monta o pedido no formato da API (`from`, `to`, `products` com cm/kg/R$).  
4. Chama `POST .../api/v2/me/shipment/calculate` (sandbox ou produção).  
5. Devolve as opções (ex.: PAC, SEDEX, Jadlog) com **preço e prazo customizados**.  
6. O cliente vê as opções e, se quiser, segue no WhatsApp.

---

## Por que esse modelo faz sentido para a Patch Works

- Vocês trabalham **sob encomenda** — o site mostra, informa e aproxima; não precisa de carrinho complexo.  
- A **cotação de frete** tira a dúvida do cliente na hora, no mesmo lugar em que ele vê o produto.  
- O **Admin** permite a dona da loja atualizar catálogo e avaliações sozinha.  
- **MySQL** prepara o projeto para crescer e para ambiente mais próximo de produção.

---

## Resumo do pitch (30 segundos)

> “A Patch Works e Afins tem um catálogo online feito sob medida para artesanato: o cliente conhece a marca, escolhe o produto, calcula o frete na hora com o Melhor Envio e chama no WhatsApp. A loja gerencia tudo pelo painel, com os dados no MySQL. Simples para quem compra, leve para quem vende.”
