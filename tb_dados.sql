CREATE DATABASE bd_sensores;

USE bd_sensores;

CREATE TABLE tb_dados(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente VARCHAR(50) NOT NULL,
    tempo_registro datetime NOT NULL,
    oximetro_saturacao_oxigenio INT,
    oximetro_frequencia_pulso INT,
    frequencia_cardiaca INT,
    temperatura DECIMAL(4, 1),
    indice_uv INT
);