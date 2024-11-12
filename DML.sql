USE bd_sensores;

DELIMITER //

CREATE PROCEDURE InsertDataOneWeek()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE dt DATETIME DEFAULT '2024-11-01 08:00:00';

    WHILE i < 1000 DO
        INSERT INTO tb_dados 
        (id_paciente, tempo_registro, oximetro_saturacao_oxigenio, oximetro_frequencia_pulso, frequencia_cardiaca, temperatura, indice_uv)
        VALUES 
        (
            'P001',
            dt + INTERVAL (i * 10) MINUTE,     -- Incremento de 10 minutos para cada registro, totalizando cerca de uma semana

            80 + (i % 16),                     -- Saturação de oxigênio variando de 80 a 95
            60 + (i % 101),                    -- Frequência de pulso variando de 60 a 160
            60 + (i % 101),                    -- Frequência cardíaca variando de 60 a 160
            31 + (i % 9),                      -- Temperatura variando de 31 a 39
            3 + (i % 9)                        -- Índice UV variando de 3 a 11
        );

        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;

-- Executar o procedimento para inserir os dados
CALL InsertDataOneWeek();

SELECT * FROM tb_dados;