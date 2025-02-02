DROP DATABASE IF EXISTS golden;
DROP USER IF EXISTS 'robot'@'localhost';
CREATE DATABASE golden;

USE golden;

CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    serial VARCHAR(100) NOT NULL UNIQUE,
    winner BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tickets(serial, winner) values ('JDHACK{The_G0lden_T1cket_1s_Y0urs}', TRUE);

CREATE USER 'robot'@'localhost' IDENTIFIED BY 'The_Am@z1ng_P@ssw0rd';
GRANT SELECT, INSERT, UPDATE, DELETE ON tickets TO 'robot'@'localhost';
FLUSH PRIVILEGES;
