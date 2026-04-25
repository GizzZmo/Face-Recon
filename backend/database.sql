CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    face_encoding BLOB,
    access_start TIME,
    access_end TIME,
    rfid_code TEXT DEFAULT NULL,
    nfc_tag TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_granted BOOLEAN,
    method TEXT DEFAULT 'face'
);
