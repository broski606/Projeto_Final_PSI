DROP DATABASE IF EXISTS Columbofilia_Armazem;
CREATE DATABASE Columbofilia_Armazem;
USE Columbofilia_Armazem;

CREATE TABLE Categoria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    designacao VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
)engine=innodb;

CREATE TABLE Fornecedor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    nif VARCHAR(20)  NOT NULL UNIQUE,
    morada VARCHAR(200),
    telefone VARCHAR(30),
    email VARCHAR(150),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
)engine=innodb;

CREATE TABLE Utilizador (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
)engine=innodb;

CREATE TABLE Loja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    nif VARCHAR(20)  NOT NULL UNIQUE,
    morada VARCHAR(200),
    email VARCHAR(150),
    telefone VARCHAR(30),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
)engine=innodb;

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
)engine=innodb;

CREATE TABLE EncomendaArmazem (
    nEncomendaArmazem INT PRIMARY KEY AUTO_INCREMENT,
    idUtilizador INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id)
)engine=innodb;

CREATE TABLE DetalheEncomendaArmazem (
    nEncomendaArmazem INT NOT NULL,
    idProduto INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (nEncomendaArmazem, idProduto),
    FOREIGN KEY (nEncomendaArmazem) REFERENCES EncomendaArmazem(nEncomendaArmazem),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
)engine=innodb;

CREATE TABLE EncomendaLoja (
    nEncomendaLoja INT PRIMARY KEY AUTO_INCREMENT,
    idUtilizador INT NOT NULL,
    idLoja INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id),
    FOREIGN KEY (idLoja) REFERENCES Loja(id)
)engine=innodb;

CREATE TABLE DetalheEncomendaLoja (
    nEncomendaLoja INT NOT NULL,
    idProduto INT NOT NULL,
    quantidade INT NOT NULL,
    precoUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (nEncomendaLoja, idProduto),
    FOREIGN KEY (nEncomendaLoja) REFERENCES EncomendaLoja(nEncomendaLoja),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
)engine=innodb;

INSERT INTO Categoria (designacao) VALUES ('Alimentação'), ('Acessórios'), ('Medicamentos');

INSERT INTO Fornecedor (nome, nif, morada, telefone, email) VALUES 
('Fornecedor A', '123456789', 'Rua A, 1', '912345678', 'a@fornecedor.com'),
('Fornecedor B', '987654321', 'Rua B, 2', '987654321', 'b@fornecedor.com');

INSERT INTO Utilizador (nome, email, password, admin) VALUES 
('Admin User', 'admin@example.com', 'password123', TRUE),
('Normal User', 'user@example.com', 'password123', FALSE);

INSERT INTO Loja (nome, nif, morada, email, telefone) VALUES 
('Loja Central', '111111111', 'Praça Central, 10', 'loja@central.com', '211111111'),
('Loja Norte', '222222222', 'Avenida Norte, 20', 'loja@norte.com', '222222222');

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock) VALUES 
(1, 1, 'Ração Premium', 10.00, 15.00, 100),
(2, 2, 'Cesto de Transporte', 50.00, 70.00, 20),
(3, 1, 'Vacina Antiparasitária', 20.00, 30.00, 50);

INSERT INTO EncomendaArmazem (idUtilizador, dataEncomenda, dataEntrega) VALUES 
(1, '2023-01-01', '2023-01-05'),
(2, '2023-02-01', NULL);

INSERT INTO DetalheEncomendaArmazem (nEncomendaArmazem, idProduto, quantidade, precoUnitario) VALUES 
(1, 1, 10, 10.00),
(1, 3, 5, 20.00),
(2, 2, 2, 50.00);

INSERT INTO EncomendaLoja (idUtilizador, idLoja, dataEncomenda, dataEntrega) VALUES 
(1, 1, '2023-03-01', '2023-03-03'),
(2, 2, '2023-04-01', NULL);

INSERT INTO DetalheEncomendaLoja (nEncomendaLoja, idProduto, quantidade, precoUnitario) VALUES 
(1, 1, 5, 15.00),
(1, 2, 1, 70.00),
(2, 3, 3, 30.00);