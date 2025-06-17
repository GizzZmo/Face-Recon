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
