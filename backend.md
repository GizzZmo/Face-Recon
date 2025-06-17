Thank you for clarifying! Here’s how we’ll proceed:

- I’ll start with the Python backend: modularized, following all 8 improvement points, with all auxiliary files (requirements.txt, config, README, etc.) and clean, English code/comments.
- I’ll present the files one by one, with clear file names.
- After the backend, I’ll move on to frontend, Solidity, and mobile in subsequent replies.

Let’s begin with the backend. The main components (based on your repo and recommendations) will be:

1. Directory Structure (in /backend and /src)
2. config.py (central configuration management)
3. main_build_database.py (face database builder)
4. main_realtime_recognition.py (real-time face recognition)
5. utils/ (utility functions)
6. server.py (Flask API backend)
7. requirements.txt
8. README.md (backend-specific)
9. .gitignore

---

### 1. Directory Structure

(For reference, not as a file)

```
Face-Recon/
│
├── backend/
│   ├── server.py
│   ├── ai_model.py
│   ├── database.sql
│   └── blockchain.sol
│
├── src/
│   ├── config.py
│   ├── main_build_database.py
│   ├── main_realtime_recognition.py
│   └── utils/
│       ├── face_utils.py
│       ├── error_handling.py
│       └── __init__.py
│
├── data/
│   ├── known_faces/
│   ├── unknown_faces/
│   └── encodings.pickle
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

### 2. backend/server.py

```python
from flask import Flask, request, jsonify
import sqlite3
from src.config import DATABASE_PATH

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/access', methods=['POST'])
def check_access():
    data = request.json
    user = data.get("user")
    if not user:
        return jsonify({"error": "User not provided"}), 400

    # Example: Just check if user exists (expand logic for your needs)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (user,))
    user_row = cursor.fetchone()
    conn.close()

    if user_row:
        return jsonify({"access": True})
    return jsonify({"access": False})

if __name__ == '__main__':
    app.run(debug=True)
```

---

### 3. backend/database.sql

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    face_encoding BLOB NOT NULL,
    access_start TIME,
    access_end TIME,
    rfid_code TEXT DEFAULT NULL,
    nfc_tag TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_granted BOOLEAN
);
```

---

### 4. src/config.py

```python
import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWN_FACES_DIR = os.path.join(DATA_DIR, "known_faces")
UNKNOWN_FACES_DIR = os.path.join(DATA_DIR, "unknown_faces")
ENCODINGS_PATH = os.path.join(DATA_DIR, "encodings.pickle")
DATABASE_PATH = os.path.join(BASE_DIR, "backend", "face_recon.db")  # SQLite DB file

# Face recognition settings
DETECTION_MODEL = "hog"  # or "cnn"
FACE_TOLERANCE = 0.6

# Other config
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
```

---

### 5. src/main_build_database.py

```python
"""
Builds the facial encoding database from known faces.
"""

import os
import pickle
from src.config import KNOWN_FACES_DIR, ENCODINGS_PATH
from src.utils.face_utils import encode_faces_in_directory
from src.utils.error_handling import safe_run, log_error

@safe_run
def main():
    print("Building face encodings database...")
    encodings, names = encode_faces_in_directory(KNOWN_FACES_DIR)
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump({"encodings": encodings, "names": names}, f)
    print(f"Database created at {ENCODINGS_PATH}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(e)
```

---

### 6. src/main_realtime_recognition.py

```python
"""
Runs real-time face recognition using webcam.
"""

import cv2
import pickle
from src.config import ENCODINGS_PATH
from src.utils.face_utils import recognize_faces_in_frame
from src.utils.error_handling import safe_run, log_error

@safe_run
def main():
    print("Starting real-time face recognition...")
    with open(ENCODINGS_PATH, "rb") as f:
        db = pickle.load(f)
        known_encodings = db["encodings"]
        known_names = db["names"]

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise IOError("Webcam not accessible.")

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame.")
                break

            names = recognize_faces_in_frame(frame, known_encodings, known_names)
            for name in names:
                print(f"Recognized: {name}")

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(e)
```

---

### 7. src/utils/face_utils.py

```python
import cv2
import face_recognition
import os
import numpy as np
from src.config import FACE_TOLERANCE, DETECTION_MODEL

def encode_faces_in_directory(directory):
    encodings = []
    names = []
    for person_name in os.listdir(directory):
        person_folder = os.path.join(directory, person_name)
        if not os.path.isdir(person_folder):
            continue
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)
            image = face_recognition.load_image_file(img_path)
            enc = face_recognition.face_encodings(image)
            if len(enc) > 0:
                encodings.append(enc[0])
                names.append(person_name)
    return encodings, names

def recognize_faces_in_frame(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model=DETECTION_MODEL)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    names = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=FACE_TOLERANCE)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        names.append(name)
    return names
```

---

### 8. src/utils/error_handling.py

```python
import traceback

def log_error(exc):
    with open("error.log", "a") as f:
        f.write(traceback.format_exc())
    print(f"Error: {exc}")

def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e)
    return wrapper
```

---

### 9. src/utils/__init__.py

```python
# Utility module initializer
```

---

### 10. requirements.txt

```text
opencv-python
face_recognition
numpy
Flask
```

---

### 11. .gitignore

```gitignore
# Python
*.pyc
__pycache__/
venv/
.env
error.log

# Data
data/encodings.pickle
logs/
*.db

# OS
.DS_Store
Thumbs.db
```

---

### 12. README.md (backend-focused)

```markdown
# Face-Recon Backend

This backend provides modular, scalable, and robust code for an AI-based face recognition access system.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Place known face images in `data/known_faces/<person_name>/`.
3. Build the face database:
    ```bash
    python src/main_build_database.py
    ```
4. Run real-time recognition:
    ```bash
    python src/main_realtime_recognition.py
    ```
5. Start the API server:
    ```bash
    python backend/server.py
    ```

## Project Structure

- **backend/**: API, ML model, database, blockchain contract
- **src/**: main scripts, configuration, utilities
- **data/**: face images, encodings
- **requirements.txt**: dependencies
- **README.md**: documentation

## Configuration

All parameters are set in `src/config.py`. Adjust model, tolerance, and paths as needed.

---

For any issues, check `error.log` or open an issue on GitHub.
```

---

Would you like to proceed with the next batch (Frontend), or review/ask for edits to any backend file first?
