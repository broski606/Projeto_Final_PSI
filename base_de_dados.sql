DROP DATABASE IF EXISTS "Columbofilia-Armazem";
CREATE DATABASE "Columbofilia-Armazem";
USE "Columbofilia-Armazem";

CREATE TABLE Produto (
    id INT PRIMARY KEY AUTO_INCREMENT,
    idCategoria INT,
    designacao VARCHAR(50),
    descricao VARCHAR(200),
    preco DECIMAL(10, 2),
    stock INT,
    FOREIGN KEY (idCategoria) REFERENCES Categoria(id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=innodb;

CREATE TABLE Categoria (
    id INT PRIMARY KEY,
    designacao VARCHAR(50)
)engine=innodb;

