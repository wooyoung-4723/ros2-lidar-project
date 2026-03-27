CREATE DATABASE egov_db;

USE egov_db;

CREATE TABLE lidardata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ranges JSON NOT NULL,
    `when` DATETIME NOT NULL,
    action VARCHAR(50) NOT NULL
);
