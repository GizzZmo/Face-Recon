"""
Face recognition utility functions for encoding and recognizing faces.
"""

import os
import sys

# Ensure the parent directory is in the path for imports to work
# This allows the module to be imported from various contexts
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import cv2
import face_recognition

from src.config import DETECTION_MODEL, FACE_TOLERANCE


def encode_faces_in_directory(directory):
    """
    Encode all faces found in subdirectories of the given directory.

    Args:
        directory: Path to directory containing subdirectories of face images.
                  Each subdirectory name should be the person's name.

    Returns:
        Tuple of (encodings, names) where encodings is a list of face encodings
        and names is a list of corresponding person names.
    """
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
    """
    Recognize faces in a video frame.

    Args:
        frame: OpenCV BGR format video frame
        known_encodings: List of known face encodings
        known_names: List of names corresponding to known encodings

    Returns:
        List of recognized names for each face found in frame.
        Returns "Unknown" for unrecognized faces.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model=DETECTION_MODEL)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    names = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_encodings, encoding, tolerance=FACE_TOLERANCE
        )
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        names.append(name)
    return names
