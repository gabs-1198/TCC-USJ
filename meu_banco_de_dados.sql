CREATE DATABASE meu_banco_de_dados;
USE meu_banco_de_dados;

CREATE TABLE dados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coluna1 VARCHAR(255),
    coluna2 VARCHAR(255),
    coluna3 VARCHAR(255)
);

INSERT INTO dados (coluna1, coluna2, coluna3) VALUES ('Valor 1A', 'Valor 2A', 'Valor 3A');
INSERT INTO dados (coluna1, coluna2, coluna3) VALUES ('Valor 1B', 'Valor 2B', 'Valor 3B');
INSERT INTO dados (coluna1, coluna2, coluna3) VALUES ('Valor 1C', 'Valor 2C', 'Valor 3C');


