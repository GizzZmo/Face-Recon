"""
Face recognition demonstration module.

Simple script to capture a face image from webcam.
For production use, see src/main_build_database.py and
src/main_realtime_recognition.py
"""

import cv2

# Initialize video capture from default camera
video_capture = cv2.VideoCapture(0)

print("Press 's' to save a face image, or 'q' to quit")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Register Face - Press 's' to save", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        cv2.imwrite("face.jpg", frame)
        print("Face image saved as face.jpg")
        break
    elif key == ord("q"):
        print("Cancelled")
        break

video_capture.release()
cv2.destroyAllWindows()
