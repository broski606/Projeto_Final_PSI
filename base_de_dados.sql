DROP DATABASE IF EXISTS "Columbofilia-Armazem";
CREATE DATABASE "Columbofilia-Armazem";
USE "Columbofilia-Armazem";
CREATE TABLE tipos_produto (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(50) NOT NULL,
    descricao   TEXT
);

CREATE TABLE tipos_movimentacao (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(50) NOT NULL,
    descricao   TEXT
);

CREATE TABLE status_movimentacao (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(50) NOT NULL,
    descricao   TEXT
);

CREATE TABLE categorias (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    descricao   TEXT
);

CREATE TABLE fornecedores (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    contato     VARCHAR(255),
    endereco    TEXT,
    telefone    VARCHAR(20),
    email       VARCHAR(100)
);

CREATE TABLE lojas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    localizacao VARCHAR(255),
    contato     VARCHAR(255),
    telefone    VARCHAR(20),
    email       VARCHAR(100)
);

CREATE TABLE produtos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    descricao       TEXT,
    tipo_id         INT NOT NULL,
    estoque         INT NOT NULL DEFAULT 0,
    categoria_id    INT,
    fornecedor_padrao_id INT,
    FOREIGN KEY (tipo_id)              REFERENCES tipos_produto(id),
    FOREIGN KEY (categoria_id)         REFERENCES categorias(id) ON DELETE SET NULL,
    FOREIGN KEY (fornecedor_padrao_id) REFERENCES fornecedores(id) ON DELETE SET NULL
);

CREATE TABLE compatibilidades (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    peca_id     INT NOT NULL,
    drone_id    INT NOT NULL,
    FOREIGN KEY (peca_id)  REFERENCES produtos(id) ON DELETE CASCADE,
    FOREIGN KEY (drone_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE movimentacoes (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    tipo_mov_id         INT NOT NULL,
    data                DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_id           INT NOT NULL DEFAULT 1,
    fornecedor_id       INT,
    loja_id             INT,
    observacoes         TEXT,
    FOREIGN KEY (tipo_mov_id)   REFERENCES tipos_movimentacao(id),
    FOREIGN KEY (status_id)     REFERENCES status_movimentacao(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id) ON DELETE SET NULL,
    FOREIGN KEY (loja_id)       REFERENCES lojas(id) ON DELETE SET NULL
);

CREATE TABLE itens_movimentacao (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    movimentacao_id INT NOT NULL,
    produto_id      INT NOT NULL,
    quantidade      INT NOT NULL,
    FOREIGN KEY (movimentacao_id) REFERENCES movimentacoes(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id)      REFERENCES produtos(id) ON DELETE RESTRICT
);