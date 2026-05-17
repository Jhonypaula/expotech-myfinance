DROP DATABASE IF EXISTS my_finance;

CREATE DATABASE my_finance;

USE my_finance;

CREATE TABLE tbl_usuarios (
    id_usuarios INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuarios VARCHAR(100) NOT NULL,
    email_usuarios VARCHAR(150) NOT NULL UNIQUE,
    senha_usuarios VARCHAR(255) NOT NULL,
    data_criacao_usuarios DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tbl_contas (
    id_contas INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome_contas VARCHAR(100) NOT NULL,
    tipo_contas ENUM('corrente', 'poupanca', 'carteira') NOT NULL,
    saldo_contas DECIMAL(10,2) DEFAULT 0.00,
    data_criacao_contas DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES tbl_usuarios(id_usuarios)
);

CREATE TABLE tbl_categorias (
    id_categorias INT AUTO_INCREMENT PRIMARY KEY,
    nome_categorias VARCHAR(100) NOT NULL UNIQUE,
    descricao_categorias VARCHAR(255)
);

CREATE TABLE tbl_transacoes (
    id_transacoes INT AUTO_INCREMENT PRIMARY KEY,
    conta_id INT NOT NULL,
    categoria_id INT,
     
    tipo_transacoes ENUM('entrada', 'saida') NOT NULL,
     
    valor_transacoes DECIMAL(10,2) NOT NULL,
     
    descricao_transacoes VARCHAR(255),
     
    data_transacao DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conta_id) REFERENCES tbl_contas(id_contas),

    FOREIGN KEY (categoria_id) REFERENCES tbl_categorias(id_categorias)
);

INSERT INTO tbl_categorias (
    nome_categorias,
    descricao_categorias
)
VALUES
('Alimentacao', 'Gastos com mercado, restaurantes e comida'),
('Transporte', 'Uber, gasolina, ônibus e transporte público'),
('Salario', 'Entradas salariais e pagamentos recebidos'),
('Lazer', 'Cinema, jogos, streaming e entretenimento'),
('Saude', 'Farmácia, consultas e exames'),
('Educacao', 'Cursos, faculdade e materiais de estudo'),
('Moradia', 'Aluguel, condomínio e contas da casa'),
('Investimentos', 'Aplicações financeiras e investimentos'),
('Compras', 'Roupas, eletrônicos e compras em geral'),
('Assinaturas', 'Netflix, Spotify e serviços recorrentes'),
('Transferencias', 'PIX, TED e transferências bancárias'),
('Outros', 'Transações diversas que não se encaixam nas demais categorias');
