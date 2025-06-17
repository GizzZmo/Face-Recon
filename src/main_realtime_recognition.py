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
