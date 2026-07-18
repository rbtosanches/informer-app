-- ========================================
-- CREATE SCHEMA
-- ========================================
CREATE SCHEMA IF NOT EXISTS system;

-- ========================================
-- TABLE: system.iaplicacoes
-- Description: Stores application definitions
-- ========================================
CREATE TABLE IF NOT EXISTS system.iaplicacoes (
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

-- Create index for frequently queried columns
CREATE INDEX idx_iaplicacoes_cod_aplic ON system.iaplicacoes(cod_aplic);
CREATE INDEX idx_iaplicacoes_ativo_aplic ON system.iaplicacoes(ativo_aplic);

-- ========================================
-- TABLE: system.iusuarios
-- Description: Stores user information
-- ========================================
CREATE TABLE IF NOT EXISTS system.iusuarios (
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

-- Create indexes for frequently queried columns
CREATE INDEX idx_iusuarios_usuario ON system.iusuarios(usuario);
CREATE INDEX idx_iusuarios_ativo_usuario ON system.iusuarios(ativo_usuario);
CREATE INDEX idx_iusuarios_email ON system.iusuarios(email_usuario);

-- ========================================
-- TABLE: system.iusuarios_iaplicacoes
-- Description: Junction table linking users to applications
-- ========================================
CREATE TABLE IF NOT EXISTS system.iusuarios_iaplicacoes (
    id_usua_aplic SERIAL PRIMARY KEY,
    id_usua INTEGER NOT NULL REFERENCES system.iusuarios(id_usua) ON DELETE CASCADE,
    id_aplic INTEGER NOT NULL REFERENCES system.iaplicacoes(id_aplic) ON DELETE CASCADE,
    ativo_usua_aplic BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usua, id_aplic)
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_iusuarios_iaplicacoes_id_usua ON system.iusuarios_iaplicacoes(id_usua);
CREATE INDEX idx_iusuarios_iaplicacoes_id_aplic ON system.iusuarios_iaplicacoes(id_aplic);
CREATE INDEX idx_iusuarios_iaplicacoes_ativo ON system.iusuarios_iaplicacoes(ativo_usua_aplic);

-- ========================================
-- ADDITIONAL INDEXES
-- ========================================
CREATE INDEX idx_iaplicacoes_created_at ON system.iaplicacoes(created_at);
CREATE INDEX idx_iusuarios_created_at ON system.iusuarios(created_at);
CREATE INDEX idx_iusuarios_iaplicacoes_created_at ON system.iusuarios_iaplicacoes(created_at);

-- ========================================
-- GRANTS (Adjust as needed)
-- ========================================
-- GRANT USAGE ON SCHEMA system TO seu_usuario;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA system TO seu_usuario;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA system TO seu_usuario;
