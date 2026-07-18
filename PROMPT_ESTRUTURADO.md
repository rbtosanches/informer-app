# PROMPT ESTRUTURADO - APLICATIVO INFORMER

## 1. OBJETIVO GERAL
Construir uma aplicação web em Python com sistema de autenticação, autorização por usuário/aplicação e CRUD completo com interface responsiva.

---

## 2. TECNOLOGIAS E DEPENDÊNCIAS

### Backend
- **Framework**: FastAPI (recomendado) ou Flask
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticação**: JWT + Password Hashing (bcrypt)
- **Dependências principais**:
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
python-multipart==0.0.6
passlib==1.7.4
bcrypt==4.1.1
PyJWT==2.8.1
```

### Frontend
- **Framework CSS**: Bootstrap 5
- **Template Engine**: Jinja2
- **JavaScript**: Vanilla JS + jQuery (opcional)
- **Datagrid**: DataTables.js com Bootstrap 5

---

## 3. ESTRUTURA DO BANCO DE DADOS

### Banco: `informer`
### Schema: `system`

#### 3.1 Tabela: `iaplicacoes`
```sql
CREATE TABLE system.iaplicacoes (
  id_aplic SERIAL PRIMARY KEY,
  cod_aplic VARCHAR(50) NOT NULL UNIQUE,
  nom_aplic VARCHAR(150) NOT NULL,
  desc_aplic TEXT,
  end_aplic VARCHAR(255),
  ativo_aplic BOOLEAN DEFAULT true,
  data_aplic DATE DEFAULT CURRENT_DATE,
  versao_aplic VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2 Tabela: `iusuarios`
```sql
CREATE TABLE system.iusuarios (
    id_usua SERIAL PRIMARY KEY,
    nom_usua VARCHAR(255) NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    nivel_usuario VARCHAR(50) DEFAULT 'usuario',
    senha_usuario VARCHAR(255) NOT NULL,
    ativo_usuario BOOLEAN DEFAULT true,
    email_usuario VARCHAR(150),
    dir_usuario VARCHAR(255),
    data_usuario DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.3 Tabela: `iusuarios_iaplicacoes`
```sql
CREATE TABLE system.iusuarios_iaplicacoes (
    id_usua_aplic SERIAL PRIMARY KEY,
    id_usua INTEGER NOT NULL REFERENCES system.iusuarios(id_usua) ON DELETE CASCADE,
    id_aplic INTEGER NOT NULL REFERENCES system.iaplicacoes(id_aplic) ON DELETE CASCADE,
    ativo_usua_aplic BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usua, id_aplic)
);
```

---

## 4. ESTRUTURA DE PASTAS DO PROJETO

```
informer-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── aplicacao.py
│   │   └── usuario_aplicacao.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── aplicacao.py
│   │   └── usuario_aplicacao.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── aplicacoes.py
│   │   └── usuarios_aplicacoes.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── aplicacao.py
│   │   └── usuario_aplicacao.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── password.py
│   │   └── jwt.py
│   └── middleware/
│       ├── __init__.py
│       └── auth.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── menu.html
│   ├── usuarios/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   ├── aplicacoes/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   └── usuarios_aplicacoes/
│       ├── list.html
│       ├── create.html
│       └── edit.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── bootstrap/ (ou via CDN)
├── scripts/
│   ├── create_tables.sql
│   ├── insert_default_data.sql
│   └── db_init.py
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

---

## 5. FLUXO DE AUTENTICAÇÃO E AUTORIZAÇÃO

### 5.1 Login
1. Usuário acessa `/login`
2. Insere nome de usuário e senha
3. Sistema valida contra tabela `iusuarios`
4. Se admin (usuário = 'admin' e senha = 's4nch3s'):
   - Acesso total a todas as aplicações
5. Se usuário comum:
   - Verifica tabela `iusuarios_iaplicacoes`
   - Apenas aplicações com `ativo_usua_aplic = true` aparecem
6. Gera JWT Token válido por 24h
7. Redireciona para `/menu`

### 5.2 Menu
- Exibe aplicações disponíveis para o usuário logado
- Construído dinamicamente conforme:
  - **Admin**: todas as aplicações com `ativo_aplic = true`
  - **Usuário**: aplicações com `ativo_aplic = true` E `ativo_usua_aplic = true`

---

## 6. ESPECIFICAÇÕES DAS APLICAÇÕES

### 6.1 Aplicação: USUÁRIOS
**Rota Base**: `/aplicacoes/usuarios`

**Funcionalidades**:
- ✅ Listar usuários com datagrid
- ✅ Filtros: nome, usuário, nível, status (ativo/inativo)
- ✅ Criar novo usuário
- ✅ Editar usuário existente
- ✅ Visualizar detalhes
- ✅ Deletar usuário (soft delete recomendado)
- ✅ Validações: email único, usuário único, senha com força mínima

### 6.2 Aplicação: APLICAÇÕES
**Rota Base**: `/aplicacoes/aplicacoes`

**Funcionalidades**:
- ✅ Listar aplicações com datagrid
- ✅ Filtros: código, nome, status (ativo/inativo)
- ✅ Criar nova aplicação
- ✅ Editar aplicação existente
- ✅ Visualizar detalhes
- ✅ Deletar aplicação (soft delete recomendado)

### 6.3 Aplicação: USUÁRIOS-APLICAÇÕES
**Rota Base**: `/aplicacoes/usuarios-aplicacoes`

**Funcionalidades**:
- ✅ Listar vinculações com datagrid
- ✅ Filtros: usuário, aplicação, status
- ✅ Vincular usuário a aplicação
- ✅ Editar autorização
- ✅ Visualizar detalhes
- ✅ Remover vinculação
- ✅ Select dinâmicos para usuário e aplicação

---

## 7. DATAGRIDS

### Requisitos por Datagrid
- Bootstrap 5 compatível
- Filtros em linha ou modal
- Paginação (10, 25, 50 registros)
- Ordenação por coluna
- Ações: View, Edit, Delete
- Responsivo mobile
- Bulk actions (opcional)

### Bibliotecas Recomendadas
- **DataTables.js**: Fácil, completa, Bootstrap 5 ready
- **AgGrid Community**: Mais robusta, livre para uso comercial
- **Bootstrap Table**: Simples e nativa ao Bootstrap

---

## 8. SEGURANÇA

- ✅ Senhas com hash bcrypt (custo 12)
- ✅ JWT para sessões (HS256)
- ✅ CSRF Protection (em formulários)
- ✅ SQL Injection prevention (via ORM)
- ✅ HTTPS recomendado em produção
- ✅ Validação de entrada (Pydantic)
- ✅ Rate limiting em `/login`
- ✅ Logs de auditoria (opcional)

---

## 9. VARIÁVEIS DE AMBIENTE (.env)

```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=informer
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_SCHEMA=system

# App
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
TOKEN_EXPIRE_HOURS=24
DEBUG=False
ADMIN_PASSWORD=s4nch3s

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 10. INSTRUÇÕES DE SETUP

### Pré-requisitos
- Python 3.9+
- PostgreSQL 12+
- pip

### Passo a Passo

```bash
# 1. Clone/crie o repositório
mkdir informer-app && cd informer-app

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edite .env com suas credenciais

# 5. Crie banco de dados e tabelas
python scripts/db_init.py

# 6. Insira dados iniciais
psql -U postgres -d informer -f scripts/insert_default_data.sql

# 7. Execute aplicação
python run.py
# Acesse: http://localhost:8000
```

---

## 11. ENDPOINTS RESUMO

### Autenticação
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /auth/me` - Dados do usuário logado

### Aplicações
- `GET /api/aplicacoes` - Listar
- `POST /api/aplicacoes` - Criar
- `GET /api/aplicacoes/{id}` - Obter
- `PUT /api/aplicacoes/{id}` - Atualizar
- `DELETE /api/aplicacoes/{id}` - Deletar

### Usuários
- `GET /api/usuarios` - Listar
- `POST /api/usuarios` - Criar
- `GET /api/usuarios/{id}` - Obter
- `PUT /api/usuarios/{id}` - Atualizar
- `DELETE /api/usuarios/{id}` - Deletar

### Usuários-Aplicações
- `GET /api/usuarios-aplicacoes` - Listar
- `POST /api/usuarios-aplicacoes` - Criar
- `GET /api/usuarios-aplicacoes/{id}` - Obter
- `PUT /api/usuarios-aplicacoes/{id}` - Atualizar
- `DELETE /api/usuarios-aplicacoes/{id}` - Deletar

---

## 12. PRÓXIMOS PASSOS

- ✅ Revisar e validar especificações
- ✅ Criar scripts SQL de criação de tabelas
- ✅ Implementar estrutura de pastas
- ✅ Configurar banco de dados
- ✅ Desenvolver camada de models (SQLAlchemy)
- ✅ Implementar segurança (JWT, bcrypt)
- ✅ Criar rotas API
- ✅ Desenvolver templates HTML/Jinja2
- ✅ Integrar Bootstrap 5 + DataTables.js
- ✅ Testes e validação
- ✅ Documentação final

---

**Versão**: 1.0  
**Data**: 2026-07-18  
**Responsável**: rbtosanches
