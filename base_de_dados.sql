DROP DATABASE IF EXISTS "Columbofilia-Armazem";
CREATE DATABASE "Columbofilia-Armazem";
USE "Columbofilia-Armazem";

-- Tabela CATEGORIA
CREATE TABLE Categoria (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    designacao  VARCHAR(100) NOT NULL,
    ativo       BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela FORNECEDOR
CREATE TABLE Fornecedor (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    nome     VARCHAR(150) NOT NULL,
    morada   VARCHAR(200),
    telefone VARCHAR(30),
    email    VARCHAR(150),
    ativo    BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela UTILIZADOR
CREATE TABLE Utilizador (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    nome     VARCHAR(150) NOT NULL,
    email    VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin    BOOLEAN NOT NULL DEFAULT FALSE,
    ativo    BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela LOJA
CREATE TABLE Loja (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    nome     VARCHAR(150) NOT NULL,
    nif      VARCHAR(20)  NOT NULL UNIQUE,
    email    VARCHAR(150),
    telefone VARCHAR(30),
    ativo    BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela PRODUTO
CREATE TABLE Produto (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    idCategoria     INT NOT NULL,
    idFornecedor    INT NOT NULL,
    designacao      VARCHAR(200) NOT NULL,
    preco           DECIMAL(10,2) NOT NULL,
    stock           INT NOT NULL DEFAULT 0,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    
    FOREIGN KEY (idCategoria)  REFERENCES Categoria(id),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id)
);

-- Tabela ENCOMENDA (cabeçalho da encomenda ao fornecedor)
CREATE TABLE Encomenda (
    nEncomenda        INT PRIMARY KEY AUTO_INCREMENT,
    idUtilizador      INT NOT NULL,
    dataEntregaLoja   DATE,                -- pode ser NULL se ainda não combinada
    
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id)
    -- Se quiseres controlo de estado: pode adicionar depois um campo estado ENUM('Pendente','Confirmada','Enviada','Entregue','Cancelada') 
);

-- Tabela DETALHE ENCOMENDA ARMAZÉM (itens da encomenda feita ao fornecedor)
CREATE TABLE DetalheEncomendaArmazem (
    nEncomenda     INT NOT NULL,
    idProduto      INT NOT NULL,
    precoUnitario  DECIMAL(10,2) NOT NULL,
    
    PRIMARY KEY (nEncomenda, idProduto),
    FOREIGN KEY (nEncomenda) REFERENCES Encomenda(nEncomenda),
    FOREIGN KEY (idProduto)  REFERENCES Produto(id)
);

-- Tabela DETALHE ENCOMENDA LOJA
CREATE TABLE DetalheEncomendaLoja (
    nEncomendaLoja   INT NOT NULL,          -- atenção: este campo parece ser uma FK ou identificador composto
    idProduto        INT NOT NULL,
    precoUnitario    DECIMAL(10,2) NOT NULL,
    
    PRIMARY KEY (nEncomendaLoja, idProduto),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
    -- Se nEncomendaLoja for FK para uma tabela EncomendaLoja (que não existe no diagrama), adicionar:
    -- FOREIGN KEY (nEncomendaLoja) REFERENCES EncomendaLoja(id)
);