CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    face_encoding LONGBLOB NOT NULL,
    access_start TIME,
    access_end TIME,
    rfid_code VARCHAR(50) DEFAULT NULL,
    nfc_tag VARCHAR(50) DEFAULT NULL
);

CREATE TABLE access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_granted BOOLEAN
);
