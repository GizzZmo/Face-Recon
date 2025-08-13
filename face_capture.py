import cv2

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    cv2.imshow('Registrer ansikt', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("face.jpg", frame)
        break

video_capture.release()
cv2.destroyAllWindows()
