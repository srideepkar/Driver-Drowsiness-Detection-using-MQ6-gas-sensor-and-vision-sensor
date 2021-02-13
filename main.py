import cv2
import numpy as np
import process
import time
from calibration.gas_detection import GasDetection

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    detection = GasDetection()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    try:
        while True:
            success, img = cap.read()
            img = cv2.filter2D(img, -1, kernel=np.array([[0, -1, 0], [-1, 5.5, -1], [0, -1, 0]], np.float32))
            img = img[:, :]
            face = face_cascade.detectMultiScale(img, 1.1, 4)
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow("video", img)
            process.process1(img)
            ppm = detection.percentage()
            print('CO: {} ppm'.format(ppm[detection.CO_GAS]))
            print('H2: {} ppm'.format(ppm[detection.H2_GAS]))
            print('CH4: {} ppm'.format(ppm[detection.CH4_GAS]))
            print('LPG: {} ppm'.format(ppm[detection.LPG_GAS]))
            print('PROPANE: {} ppm'.format(ppm[detection.PROPANE_GAS]))
            print('ALCOHOL: {} ppm'.format(ppm[detection.ALCOHOL_GAS]))
            print('SMOKE: {} ppm\n'.format(ppm[detection.SMOKE_GAS]))
    except KeyboardInterrupt:
        print('\nAborted by user!')
