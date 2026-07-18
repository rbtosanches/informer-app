-- ========================================
-- INSERT DEFAULT DATA
-- ========================================

-- ========================================
-- INSERT INTO iaplicacoes
-- ========================================
INSERT INTO system.iaplicacoes (cod_aplic, nom_aplic, desc_aplic, end_aplic, ativo_aplic, versao_aplic)
VALUES 
    ('APP_USUARIOS', 'Gerenciador de Usuários', 'Aplicação para gerenciar usuários do sistema', '/aplicacoes/usuarios', true, '1.0.0'),
    ('APP_APLICACOES', 'Gerenciador de Aplicações', 'Aplicação para gerenciar aplicações disponíveis', '/aplicacoes/aplicacoes', true, '1.0.0'),
    ('APP_USUARIOS_APLICACOES', 'Permissões', 'Aplicação para vincular usuários a aplicações', '/aplicacoes/usuarios-aplicacoes', true, '1.0.0'),
    ('APP_RELATORIOS', 'Relatórios', 'Aplicação para gerar relatórios do sistema', '/aplicacoes/relatorios', false, '1.0.0'),
    ('APP_CONFIGURACOES', 'Configurações', 'Aplicação para configurar o sistema', '/aplicacoes/configuracoes', false, '1.0.0')
ON CONFLICT (cod_aplic) DO NOTHING;

-- ========================================
-- INSERT INTO iusuarios
-- Note: Password is hashed with bcrypt
-- admin / s4nch3s (bcrypt hash - you should regenerate this)
-- ========================================
INSERT INTO system.iusuarios (nom_usua, usuario, nivel_usuario, senha_usuario, ativo_usuario, email_usuario, dir_usuario)
VALUES 
    ('Administrador', 'admin', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUVqKSDi', true, 'admin@informer.com', '/home/admin'),
    ('Roberto Sanches', 'rbtosanches', 'usuario', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUVqKSDi', true, 'rbtosanches@gmail.com', '/home/rbtosanches'),
    ('Usuário Teste', 'usuario_teste', 'usuario', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUVqKSDi', true, 'teste@informer.com', '/home/teste')
ON CONFLICT (usuario) DO NOTHING;

-- ========================================
-- INSERT INTO iusuarios_iaplicacoes
-- Admin has access to all applications
-- Other users have limited access
-- ========================================

-- Admin (id_usua = 1) gets access to all active applications
INSERT INTO system.iusuarios_iaplicacoes (id_usua, id_aplic, ativo_usua_aplic)
SELECT 1, id_aplic, true
FROM system.iaplicacoes
WHERE ativo_aplic = true
ON CONFLICT (id_usua, id_aplic) DO NOTHING;

-- User rbtosanches (id_usua = 2) gets access to users, applications, and permissions
INSERT INTO system.iusuarios_iaplicacoes (id_usua, id_aplic, ativo_usua_aplic)
VALUES 
    (2, (SELECT id_aplic FROM system.iaplicacoes WHERE cod_aplic = 'APP_USUARIOS'), true),
    (2, (SELECT id_aplic FROM system.iaplicacoes WHERE cod_aplic = 'APP_APLICACOES'), true),
    (2, (SELECT id_aplic FROM system.iaplicacoes WHERE cod_aplic = 'APP_USUARIOS_APLICACOES'), true)
ON CONFLICT (id_usua, id_aplic) DO NOTHING;

-- User usuario_teste (id_usua = 3) gets access only to users application
INSERT INTO system.iusuarios_iaplicacoes (id_usua, id_aplic, ativo_usua_aplic)
VALUES 
    (3, (SELECT id_aplic FROM system.iaplicacoes WHERE cod_aplic = 'APP_USUARIOS'), true)
ON CONFLICT (id_usua, id_aplic) DO NOTHING;

-- ========================================
-- VERIFY DATA
-- ========================================
SELECT 'Aplicações' as tipo, COUNT(*) as total FROM system.iaplicacoes
UNION ALL
SELECT 'Usuários', COUNT(*) FROM system.iusuarios
UNION ALL
SELECT 'Usuários-Aplicações', COUNT(*) FROM system.iusuarios_iaplicacoes;
