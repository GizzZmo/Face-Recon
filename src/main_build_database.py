"""
Builds the facial encoding database from known faces.
"""

import os
import sys

# Ensure the parent directory is in the path for imports to work
# This allows running both as `python src/main_build_database.py`
# and as `python -m src.main_build_database`
if __name__ == "__main__":
    # Add parent directory to path if running as script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

import pickle

from src.config import ENCODINGS_PATH, KNOWN_FACES_DIR
from src.utils.error_handling import log_error, safe_run
from src.utils.face_utils import encode_faces_in_directory


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
