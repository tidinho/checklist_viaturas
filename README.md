# 🚓 Sistema de Checklist de Viaturas

Sistema web desenvolvido em **Django** para controle e registro de **checklist de viaturas policiais**, permitindo registrar condições da viatura, anexar fotos e gerar relatórios em PDF.

---

## 📋 Funcionalidades

* Cadastro de viaturas
* Cadastro de policiais
* Registro de checklist diário
* Upload de múltiplas fotos
* Extração de metadados das imagens
* Visualização das fotos do checklist
* Geração de relatório em PDF
* Controle de acesso por usuário
* Painel administrativo

---

## 🛠 Tecnologias utilizadas

* Python
* Django
* Bootstrap
* SQLite
* HTML5
* CSS3
* JavaScript

---

## 📂 Estrutura do Projeto

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
│   ├── admin.py
│   └── templates/
│
├── static/
├── media/
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/tidinho/checklist_viaturas.git
```

Entre na pasta:

```bash
cd checklist_viaturas
```

Crie ambiente virtual:

```bash
python3 -m venv venv
```

Ative:

```bash
source venv/bin/activate
```

Instale dependências:

```bash
pip install -r requirements.txt
```

Execute migrações:

```bash
python manage.py migrate
```

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse:

```
http://127.0.0.1:8000
```

---

## 📸 Funcionalidades do Checklist

O sistema permite registrar:

* Quilometragem
* Combustível
* Estado geral da viatura
* Fotos da inspeção
* Data e hora do registro
* Policial responsável

---

## 📄 Relatórios

O sistema gera **relatórios em PDF contendo:**

* Dados da viatura
* Informações do checklist
* Fotos anexadas
* Data e usuário responsável

---

## 🔒 Controle de acesso

O sistema possui:

* Login de usuário
* Permissões administrativas
* Controle de acesso aos módulos

---

## 👨‍💻 Autor

Desenvolvido por **Tidinho**

Sistema para controle operacional de viaturas.

---

## 📜 Licença

Projeto de uso interno.
