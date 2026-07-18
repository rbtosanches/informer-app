# Informer - Sistema de Gestão

Aplicação web completa em Python com sistema de autenticação, autorização por usuário/aplicação e CRUD com interface responsiva.

## 🚀 Features

- ✅ Autenticação com JWT
- ✅ Autorização por usuário e aplicação
- ✅ CRUD completo de Usuários
- ✅ CRUD completo de Aplicações
- ✅ Gerenciamento de Permissões (Usuário-Aplicação)
- ✅ Interface responsiva com Bootstrap 5
- ✅ DataTables para listagens com filtros
- ✅ Banco de dados PostgreSQL
- ✅ Segurança com bcrypt e JWT

## 📋 Pré-requisitos

- Python 3.9+
- PostgreSQL 12+
- pip

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/rbtosanches/informer-app.git
cd informer-app
```

### 2. Crie e ative o ambiente virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 5. Inicialize o banco de dados

```bash
python scripts/db_init.py
```

### 6. Execute a aplicação

```bash
python run.py
```

A aplicação estará disponível em: http://localhost:8000

## 🔑 Credenciais Padrão

- **Usuário**: admin
- **Senha**: s4nch3s

## 📁 Estrutura do Projeto

```
informer-app/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API routes
│   ├── crud/            # CRUD operations
│   ├── security/        # Authentication & Security
│   ├── middleware/      # Custom middleware
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── scripts/             # Database scripts
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── run.py              # Entry point
```

## 🔌 API Endpoints

### Autenticação
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /auth/me` - Dados do usuário

### Usuários
- `GET /api/usuarios` - Listar usuários
- `POST /api/usuarios` - Criar usuário
- `GET /api/usuarios/{id}` - Obter usuário
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Deletar usuário

### Aplicações
- `GET /api/aplicacoes` - Listar aplicações
- `POST /api/aplicacoes` - Criar aplicação
- `GET /api/aplicacoes/{id}` - Obter aplicação
- `PUT /api/aplicacoes/{id}` - Atualizar aplicação
- `DELETE /api/aplicacoes/{id}` - Deletar aplicação

### Permissões
- `GET /api/usuarios-aplicacoes` - Listar permissões
- `POST /api/usuarios-aplicacoes` - Criar permissão
- `GET /api/usuarios-aplicacoes/{id}` - Obter permissão
- `PUT /api/usuarios-aplicacoes/{id}` - Atualizar permissão
- `DELETE /api/usuarios-aplicacoes/{id}` - Deletar permissão

## 🛡️ Segurança

- Senhas hasheadas com bcrypt
- Autenticação via JWT
- Proteção CSRF em formulários
- Validação de entrada com Pydantic
- Prevenção de SQL Injection via ORM
- Rate limiting em login

## 📝 Banco de Dados

### Schema: system

#### Tabelas
- `iaplicacoes` - Aplicações do sistema
- `iusuarios` - Usuários do sistema
- `iusuarios_iaplicacoes` - Permissões

## 🚢 Deployment

Para produção, recomenda-se:

1. Usar HTTPS
2. Definir `DEBUG=False`
3. Usar variáveis de ambiente seguras
4. Usar um servidor WSGI como Gunicorn
5. Configurar um reverse proxy (nginx, Apache)
6. Usar um banco de dados dedicado

## 📄 Documentação

Ver `PROMPT_ESTRUTURADO.md` para especificações completas do projeto.

## 👤 Autor

Roberto Sanches (rbtosanches)

## 📅 Versão

1.0.0 - 2026-07-18

## 📜 Licença

MIT License
