DROP DATABASE IF EXISTS "Columbofilia-Armazem";
CREATE DATABASE "Columbofilia-Armazem";
USE "Columbofilia-Armazem";

CREATE TABLE Categoria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    designacao VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Fornecedor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    nif VARCHAR(20)  NOT NULL UNIQUE,
    morada VARCHAR(200),
    telefone VARCHAR(30),
    email VARCHAR(150),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Utilizador (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Loja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    nif VARCHAR(20)  NOT NULL UNIQUE,
    morada VARCHAR(200),
    email VARCHAR(150),
    telefone VARCHAR(30),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Produto (
    id INT PRIMARY KEY AUTO_INCREMENT,
    idCategoria INT NOT NULL,
    idFornecedor INT NOT NULL,
    designacao VARCHAR(200) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    precoRevenda DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    
    FOREIGN KEY (idCategoria) REFERENCES Categoria(id),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id)
);

CREATE TABLE EncomendaArmazem (
    nEncomendaArmazem INT PRIMARY KEY AUTO_INCREMENT,
    idUtilizador INT NOT NULL,
    idFornecedor INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL COMMENT,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id)
);

CREATE TABLE DetalheEncomendaArmazem (
    nEncomendaArmazem INT NOT NULL,
    idProduto INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (nEncomendaArmazem, idProduto),
    FOREIGN KEY (nEncomendaArmazem) REFERENCES EncomendaArmazem(nEncomendaArmazem),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
);

CREATE TABLE EncomendaLoja (
    nEncomendaLoja INT PRIMARY KEY AUTO_INCREMENT,
    idUtilizador INT NOT NULL,
    idLoja INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id),
    FOREIGN KEY (idLoja) REFERENCES Loja(id)
);

CREATE TABLE DetalheEncomendaLoja (
    nEncomendaLoja INT NOT NULL,
    idProduto INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (nEncomendaLoja, idProduto),
    FOREIGN KEY (nEncomendaLoja) REFERENCES EncomendaLoja(nEncomendaLoja),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
);