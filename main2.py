import cv2
import numpy as np
import process

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        success, img = cap.read()
        img = cv2.filter2D(img, -1, kernel=np.array([[0, -1, 0], [-1, 5.5, -1], [0, -1, 0]], np.float32))
        img = img[:, :]
        face = face_cascade.detectMultiScale(img, 1.1, 4)
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("video", img)
        process.process1(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
