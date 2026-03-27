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
    idFornecedor INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id)
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
    idFornecedor INT NOT NULL,
    idLoja INT NOT NULL,
    dataEncomenda DATE NOT NULL,
    dataEntrega DATE NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (idUtilizador) REFERENCES Utilizador(id),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id),
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

-- Dados de Teste
INSERT INTO Categoria (designacao, ativo) VALUES 
('Motores', 1),
('Controladores', 1),
('Baterias', 1),
('Estruturas', 1),
('Sensores', 1),
('Cabos e Conectores', 1),
('Componentes Eletrónicos', 1);

INSERT INTO Fornecedor (nome, nif, morada, telefone, email, ativo) VALUES 
('TechMotors Portugal', '123456789', 'Rua das Tecnologias, 45 - Porto', '220123456', 'contact@techmotors.pt', 1),
('ElectroDrone Solutions', '987654321', 'Avenida da Inovação, 78 - Lisboa', '217654321', 'vendas@electrodrone.pt', 1),
('BateryPower Systems', '456789123', 'Estrada Industrial, 12 - Aveiro', '234567890', 'info@baterypower.pt', 1),
('Estruturas Avançadas', '789123456', 'Largo da Indústria, 99 - Braga', '253456789', 'strutures@avancadas.pt', 1),
('SensorTech Ibérica', '321654987', 'Parque Tecnológico, 23 - Covilhã', '275123456', 'support@sensortech.pt', 1);

INSERT INTO Loja (nome, nif, morada, email, telefone, ativo) VALUES 
('Columbofilia Store Porto', '111222333', 'Rua Central, 100 - Porto', 'store1@columbofilia.pt', '220999888', 1),
('Loja Tecnológica Lisboa', '222333444', 'Avenida Principal, 200 - Lisboa', 'store2@columbofilia.pt', '217888777', 1);

INSERT INTO Utilizador (nome, email, password, admin) VALUES 
('Admin', 'admin@columbofilia.pt', '$2b$12$L5sGSFi.349RNBZJK/op7.UWBAcnFck6KMRjVh1lfMIZohTc3huny', 1),
('João Silva', 'joao.silva@columbofilia.pt', '$2b$12$L5sGSFi.349RNBZJK/op7.UWBAcnFck6KMRjVh1lfMIZohTc3huny', 0),
('Maria Santos', 'maria.santos@columbofilia.pt', '$2b$12$L5sGSFi.349RNBZJK/op7.UWBAcnFck6KMRjVh1lfMIZohTc3huny', 0);

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Motores
(1, 1, 'Motor Brushless 2300KV', 45.50, 65.00, 25, 1),
(1, 1, 'Motor Brushless 2700KV', 48.99, 70.00, 18, 1),
(1, 1, 'Motor DC 12V 200W', 35.00, 50.00, 30, 1),
(1, 1, 'Motor Servo Standard', 12.50, 18.00, 45, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Controladores
(2, 2, 'Controlador ESC 30A', 25.99, 38.00, 20, 1),
(2, 2, 'Controlador ESC 50A', 35.50, 52.00, 15, 1),
(2, 2, 'Placa Controlo Automatizada', 89.99, 130.00, 8, 1),
(2, 2, 'Receptor RF 2.4GHz', 22.00, 32.00, 22, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Baterias
(3, 3, 'Bateria LiPo 3S 2200mAh', 18.50, 27.00, 50, 1),
(3, 3, 'Bateria LiPo 4S 3000mAh', 24.99, 37.00, 35, 1),
(3, 3, 'Bateria NiMH 8.4V 2000mAh', 12.00, 17.50, 40, 1),
(3, 3, 'Carregador Rápido Bateria', 42.50, 62.00, 12, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Estruturas
(4, 4, 'Frame Quadcopter 450mm', 55.00, 80.00, 14, 1),
(4, 4, 'Braços em Fibra de Carbono', 28.50, 42.00, 32, 1),
(4, 4, 'Chassis Alumínio Reforçado', 68.00, 100.00, 9, 1),
(4, 4, 'Suporte Câmara Gimbal', 15.99, 23.00, 26, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Sensores
(5, 5, 'Sensor IMU 6 Eixos', 32.00, 47.00, 11, 1),
(5, 5, 'Sensor Barométrico Altitude', 18.75, 27.00, 19, 1),
(5, 5, 'Câmara FHD 1080p', 95.50, 140.00, 6, 1),
(5, 5, 'Sensor GPS u-blox NEO-7M', 22.99, 34.00, 13, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Cabos e Conectores
(6, 1, 'Conector XT60 (5 pcs)', 8.50, 12.00, 80, 1),
(6, 1, 'Conector Banana 4mm (10 pcs)', 6.99, 10.00, 100, 1),
(6, 2, 'Cabo USB Tipo C 2m', 7.50, 11.00, 45, 1),
(6, 2, 'Falsa Carga CXA 5.5mm', 3.99, 6.00, 120, 1)

INSERT INTO Produto (idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES 
-- Componentes Eletrónicos
(7, 5, 'Resistências Variadas Kit', 9.99, 14.50, 55, 1),
(7, 5, 'Condensadores Electroliticos Kit', 11.50, 17.00, 40, 1),
(7, 1, 'Microcontrolador ATmega328', 5.75, 8.50, 35, 1),
(7, 2, 'Circuito Integrado IC74HC595', 2.99, 4.50, 70, 1)
-- Encomendas de Teste

INSERT INTO EncomendaArmazem (idUtilizador, idFornecedor, dataEncomenda, dataEntrega, ativo) VALUES
(1, 1, '2026-03-01', '2026-03-05', 1), -- Encomenda entregue - TechMotors Portugal
(2, 2, '2026-03-10', NULL, 1), -- Encomenda por entregar - ElectroDrone Solutions
(3, 3, '2026-03-15', NULL, 1), -- Encomenda por entregar - BateryPower Systems
(1, 4, '2026-02-20', '2026-02-25', 1), -- Encomenda entregue - Estruturas Avançadas
(2, 5, '2026-03-20', NULL, 0); -- Encomenda cancelada - SensorTech Ibérica

INSERT INTO DetalheEncomendaArmazem (nEncomendaArmazem, idProduto, quantidade, precoUnitario) VALUES
-- Encomenda 1 (TechMotors - Motores)
(1, 1, 5, 45.50), -- Motor Brushless 2300KV
(1, 2, 3, 48.99), -- Motor Brushless 2700KV
(1, 3, 8, 35.00), -- Motor DC 12V 200W
-- Encomenda 2 (ElectroDrone - Controladores)
(2, 5, 10, 25.99), -- Controlador ESC 30A
(2, 6, 5, 35.50), -- Controlador ESC 50A
(2, 7, 2, 89.99), -- Placa Controlo Automatizada
-- Encomenda 3 (BateryPower - Baterias)
(3, 9, 20, 18.50), -- Bateria LiPo 3S 2200mAh
(3, 10, 15, 24.99), -- Bateria LiPo 4S 3000mAh
(3, 12, 5, 42.50), -- Carregador Rápido Bateria
-- Encomenda 4 (Estruturas Avançadas - Estruturas)
(4, 13, 3, 55.00), -- Frame Quadcopter 450mm
(4, 14, 10, 28.50), -- Braços em Fibra de Carbono
(4, 15, 2, 68.00), -- Chassis Alumínio Reforçado
-- Encomenda 5 (SensorTech - Sensores) - CANCELADA
(5, 17, 5, 32.00), -- Sensor IMU 6 Eixos
(5, 18, 8, 18.75); -- Sensor Barométrico Altitude
INSERT INTO EncomendaLoja (idUtilizador, idFornecedor, idLoja, dataEncomenda, dataEntrega, ativo) VALUES
(1, 1, 1, '2026-03-02', '2026-03-06', 1), -- Encomenda entregue - TechMotors para Porto
(2, 2, 2, '2026-03-12', NULL, 1), -- Encomenda por entregar - ElectroDrone para Lisboa
(3, 3, 1, '2026-03-18', NULL, 1), -- Encomenda por entregar - BateryPower para Porto
(1, 5, 2, '2026-02-22', '2026-02-27', 1); -- Encomenda entregue - SensorTech para Lisboa
INSERT INTO DetalheEncomendaLoja (nEncomendaLoja, idProduto, quantidade, precoUnitario) VALUES
-- Encomenda Loja 1 (TechMotors para Porto)
(1, 1, 2, 65.00), -- Motor Brushless 2300KV (preço revenda)
(1, 4, 5, 18.00), -- Motor Servo Standard (preço revenda)
-- Encomenda Loja 2 (ElectroDrone para Lisboa)
(2, 5, 3, 38.00), -- Controlador ESC 30A (preço revenda)
(2, 8, 4, 32.00), -- Receptor RF 2.4GHz (preço revenda)
-- Encomenda Loja 3 (BateryPower para Porto)
(3, 9, 8, 27.00), -- Bateria LiPo 3S 2200mAh (preço revenda)
(3, 11, 6, 17.50), -- Bateria NiMH 8.4V 2000mAh (preço revenda)
-- Encomenda Loja 4 (SensorTech para Lisboa)
(4, 17, 2, 47.00), -- Sensor IMU 6 Eixos (preço revenda)
(4, 20, 1, 34.00); -- Sensor GPS u-blox NEO-7M (preço revenda)