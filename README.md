# 🧵 Patch Works e Afins

**Versão 2.0** (branch `v2.0`) — evolução acadêmica da v1.0 disponível em `main`.

Projeto desenvolvido com **Python + Django** para criação de um catálogo online de produtos artesanais.

A proposta do sistema é permitir a exposição de produtos, avaliações de clientes, cotação de frete e contato com o vendedor.

---

## 🚀 Tecnologias utilizadas

- ![Python](https://img.shields.io/badge/Python-3.x-blue)
- ![Django](https://img.shields.io/badge/Django-Framework-green)
- ![HTML](https://img.shields.io/badge/HTML-5-orange)
- ![CSS](https://img.shields.io/badge/CSS-3-blue)
- ![MySQL](https://img.shields.io/badge/MySQL-8-blue)
- Melhor Envio (cotação de frete) + ViaCEP

---

## 📸 Funcionalidades
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
- ✅ Painel administrativo (Django Admin)  
- ✅ Página inicial com apresentação da loja  
- ✅ Menu de navegação (Início, Produtos, Avaliações, Contato)  
- ✅ Sistema de avaliações com imagem + link externo 
- ✅ Layout moderno e responsivo (identidade artesanal)
- ✅ Banco MySQL
- ✅ Cotação de frete (Melhor Envio) no modal do produto
- ✅ Validação de CEP (ViaCEP)
- ✅ Manuais em `docs/`

### Branches no GitHub

| Branch | Versão |
|--------|--------|
| `main` | **1.0** (versão original) |
| `v2.0` | **2.0** (MySQL, UX, Melhor Envio, docs) |

---
### 📖 Bibliografia

1. MENEZES, Nilo. *Introdução à Programação com Python: Algoritmos e lógica de programação para iniciantes*. 4. ed. São Paulo: Novatec, 2024.

2. SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. *Sistemas de Banco de Dados*. 6. ed. Rio de Janeiro: Elsevier, 2012.  
   Disponível em: https://integrada.minhabiblioteca.com.br/reader/books/9788595157552

3. GAMMA, Erich; HELM, Richard; JOHNSON, Ralph; VLISSIDES, John. *Padrões de Projeto: Soluções reutilizáveis de software orientado a objetos*. Porto Alegre: Bookman, 2000.  
   Disponível em: https://integrada.minhabiblioteca.com.br/reader/books/9788577800469

4. DJANGO SOFTWARE FOUNDATION. *Documentação oficial do Django*.  
   Disponível em: https://docs.djangoproject.com/pt-br/  
   Acesso em: 2026.

5. MOZILLA FOUNDATION. *MDN Web Docs: HTML e CSS*.  
   Disponível em: https://developer.mozilla.org/pt-BR/  
   Acesso em: 2026.

6. SOMMERVILLE, Ian. *Engenharia de Software*. 8. ed. São Paulo: Pearson, 2007.  
   Disponível em: https://plataforma.bvirtual.com.br/Acervo/Publicacao/276

7. W3SCHOOLS. *Django Tutorial*.  
   Disponível em: https://www.w3schools.com/django/django_intro.php

8. SILVA, Tiago. *Django de A a Z: crie aplicações web rápidas, seguras e escaláveis com Python*. 9. ed. São Paulo: Casa do Código, 2021.  
   Disponível em: https://plataforma.bvirtual.com.br  
   Acesso em: 23 mar 2026.

9. BHARGAVA, Aditya Y. *Entendendo Algoritmos: Um guia ilustrado para programadores e outros curiosos*. 1. ed. São Paulo: Novatec, 2015.

## ⚙️ Como rodar o projeto

### 1. Clonar repositório

```bash
git clone https://github.com/Gentilneto/patchworks.git
cd patchworks

2. Criar ambiente virtual
	python -m venv venv

Ativar o venv
venv\Scripts\activate   # Windows

3. Instalar a dependência 
	pip install django

4. rodas as migrações
	python manage.py migrate

5. Criar user admin
	python manage.py createsuperuser

6. Rodar o server
	python manage.py runserver

acessar via 
	http://127.0.0.1:8000/admin

Estrutura do projeto 

	core/
	 ├── models.py
 	 ├── views.py
	 ├── templates/
 	 ├── static/

	patchworks/
 	 ├── settings.py
 	 ├── urls.py

	manage.py

📌 Manuais de manutenção
  docs/README.md — índice
  docs/MANUAL_MANUTENCAO.md
  docs/MANUAL_API.md
  docs/MANUAL_MELHOR_ENVIO.md
  docs/MANUAL_CLOUDFLARE.md

📌 Próximas melhorias
  Cadastro de produtos via admin
  Upload de imagens com armazenamento persistente
  Deploy em produção (Render/Railway/VPS)
  Melhorias no design (UI/UX)
  integração com banco mysql
  renovação automática do refresh_token Melhor Envio

```
⚠️ Este repositório contém banco e mídias apenas para fins acadêmicos e colaboração em equipe.