CREATE DATABASE industria;
USE industria;

CREATE TABLE equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    localizacao VARCHAR(100) NOT NULL
);
CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano INT NOT NULL,
    cor VARCHAR(50) NOT NULL
);
CREATE TABLE dispositivos_de_seguranca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    localizacao VARCHAR(100) NOT NULL
);
CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);
CREATE TABLE centros_acesso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
CREATE TABLE funcionarios_centros (
    funcionario_id INT,
    centro_id INT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (centro_id) REFERENCES centros_acesso(id)
);

INSERT INTO equipamentos (nome, marca, quantidade, localizacao) VALUES
('Furadeira', 'Bosch', 10, 'Setor A'),
('Serra Circular', 'Makita', 5, 'Setor B'),
('Soldadora', 'Esab', 3, 'Setor C'),
('Compressor', 'Schulz', 2, 'Setor D');
INSERT INTO veiculos (marca, modelo, ano, cor) VALUES
('Ford', 'F-250', 2020, 'Branco'),
('Volkswagen', 'Delivery', 2019, 'Azul'),
('Mercedes-Benz', 'Actros', 2021, 'Preto'),
('Scania', 'R500', 2022, 'Vermelho');
INSERT INTO dispositivos_de_seguranca (nome, marca, quantidade, localizacao) VALUES
('Extintor', 'Lion', 20, 'Setor A'),
('Alarme', 'Intelbras', 15, 'Setor B'),
('Câmera de Segurança', 'Hikvision', 8, 'Setor C'),
('Sensor de Fumaça', 'Tyco', 12, 'Setor D');
INSERT INTO funcionarios (nome, cargo, matricula, senha) VALUES
('João Silva', 'Operário', 'OP123', 'senha123'),
('Maria Souza', 'Gerente', 'GE456', 'senha456'),
('Carlos Lima', 'Administrador de Segurança', 'AS789', 'senha789');
INSERT INTO centros_acesso (nome) VALUES
('Centro Operacional'),
('Centro de Vídeo Monitoramento'),
('Centro de Processamento de Dados');
-- Operário (João Silva) tem acesso ao Centro Operacional
INSERT INTO funcionarios_centros (funcionario_id, centro_id) VALUES
(1, 1);

-- Gerente (Maria Souza) tem acesso ao Centro Operacional e Centro de Vídeo Monitoramento
INSERT INTO funcionarios_centros (funcionario_id, centro_id) VALUES
(2, 1),
(2, 2);

-- Administrador (Carlos Lima) tem acesso a todos os centros
INSERT INTO funcionarios_centros (funcionario_id, centro_id) VALUES
(3, 1),
(3, 2),
(3, 3);

SELECT * FROM equipamentos;

SELECT * FROM veiculos;