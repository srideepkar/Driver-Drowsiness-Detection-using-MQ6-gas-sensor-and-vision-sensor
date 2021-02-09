import cv2
import numpy as np

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        success, img = cap.read()
        cv2.imshow("video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break