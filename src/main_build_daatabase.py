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
