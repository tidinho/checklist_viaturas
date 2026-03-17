# 🚓 Sistema de Checklist de Viaturas

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Django](https://img.shields.io/badge/Django-Framework-green?style=for-the-badge\&logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge\&logo=bootstrap)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge\&logo=github)

</p>

---

## 📖 Sobre o Projeto

Sistema web desenvolvido com **Django** para gerenciamento de **checklists de viaturas**, permitindo registrar inspeções operacionais, anexar fotos e gerar relatórios em PDF.

O sistema foi criado para **controle operacional de viaturas**, garantindo rastreabilidade das inspeções realizadas pelos policiais.

---

# 🎥 Demonstração do Sistema

<p align="center">
<img src="docs/sistema.gif" width="800">
</p>

---

# 📸 Telas do Sistema

### 🔐 Login

<img src="docs/login.png" width="800">

### 🚓 Cadastro de Viatura

<img src="docs/viaturas.png" width="800">

### 📋 Checklist

<img src="docs/checklist.png" width="800">

### 📄 Relatório PDF

<img src="docs/pdf.png" width="800">

---

# ⚙️ Tecnologias Utilizadas

* Python
* Django
* Bootstrap
* SQLite
* HTML5
* CSS3
* JavaScript
* ReportLab (PDF)

---

# 📂 Estrutura do Projeto

```
checklist_viaturas/
│
├── manage.py
├── db.sqlite3
│
├── viaturas/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
├── media/
├── docs/
│
└── README.md
```

---

# ⚙️ Instalação

Clone o projeto:

```
git clone https://github.com/tidinho/checklist_viaturas.git
```

Entre na pasta:

```
cd checklist_viaturas
```

Crie ambiente virtual:

```
python3 -m venv venv
```

Ative o ambiente:

```
source venv/bin/activate
```

Instale dependências:

```
pip install -r requirements.txt
```

Execute migrações:

```
python manage.py migrate
```

Crie administrador:

```
python manage.py createsuperuser
```

Inicie o servidor:

```
python manage.py runserver
```

Acesse:

```
http://127.0.0.1:8000
```

---

# 📄 Relatórios

O sistema gera **relatórios em PDF contendo:**

* Informações da viatura
* Dados do checklist
* Fotos anexadas
* Data e hora da inspeção
* Policial responsável

---

# 🚀 Deploy

O projeto pode ser publicado em:

* Render
* Railway
* Heroku
* VPS Linux

Execução em produção:

```
gunicorn checklist_viaturas.wsgi
```

---

# 📊 Estatísticas do GitHub

<p align="center">

<img height="180em" src="https://github-readme-stats.vercel.app/api?username=tidinho&show_icons=true&theme=tokyonight"/>

<img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=tidinho&layout=compact&theme=tokyonight"/>

</p>

---

# 🛣 Roadmap

Melhorias planejadas:

* Dashboard com gráficos
* Banco PostgreSQL
* API REST
* Aplicativo Mobile
* Geolocalização das fotos

---

# 👨‍💻 Autor

**Tidinho**

Projeto desenvolvido para **controle operacional de viaturas e inspeções policiais**.

---

# ⭐ Contribuição

Contribuições são bem-vindas.

1. Faça um fork
2. Crie uma branch
3. Commit suas mudanças
4. Abra um Pull Request

---

# 📜 Licença

Projeto de uso interno.
