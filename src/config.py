"""
Configuration settings for Face-Recon Security System.

This module contains all configuration variables including paths,
face recognition settings, and other system parameters.
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWN_FACES_DIR = os.path.join(DATA_DIR, "known_faces")
UNKNOWN_FACES_DIR = os.path.join(DATA_DIR, "unknown_faces")
ENCODINGS_PATH = os.path.join(DATA_DIR, "encodings.pickle")
DATABASE_PATH = os.path.join(BASE_DIR, "backend", "face_recon.db")  # SQLite DB file

# Face recognition settings
DETECTION_MODEL = "hog"  # or "cnn" for GPU-accelerated detection
FACE_TOLERANCE = 0.6  # Lower is more strict (0.0-1.0)

# Other config
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
