# 🧵 Patch Works e Afins

Projeto desenvolvido com **Python + Django** para criação de um catálogo online de produtos artesanais.

A proposta do sistema é permitir a exposição de produtos, avaliações de clientes e contato com o vendedor.

---

## 🚀 Tecnologias utilizadas

- Python 3
- Django
- HTML5
- CSS3
- SQLite (banco padrão do Django)

---

## 📸 Funcionalidades

✅ Página inicial com apresentação da loja  
✅ Menu de navegação (Início, Produtos, Avaliações, Contato)  
✅ Sistema de avaliações com imagem + link externo  
✅ Painel administrativo (Django Admin)  
✅ Layout moderno e responsivo  

---


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

6. Rodas server
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

📌 Próximas melhorias
  Cadastro de produtos via admin
  Upload de imagens com armazenamento persistente
  Deploy em produção
  Melhorias no design (UI/UX)
  integração com banco mysql
