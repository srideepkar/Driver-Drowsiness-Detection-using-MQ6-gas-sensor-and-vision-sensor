import cv2
import numpy as np
import process
import time
from calibration.gas_detection import GasDetection

def gascheck():
    ppm = detection.percentage()
    mean = (ppm[detection.CO_GAS] + ppm[detection.CH4_GAS] + ppm[detection.LPG_GAS] + ppm[detection.PROPANE_GAS] + ppm[detection.ALCOHOL_GAS] + ppm[detection.SMOKE_GAS]) / 6
    print(mean)
    if(mean>1):
        return True
    else:
        return False
if __name__ == '__main__':
    
    print("Calibrating Sensor..")
    detection = GasDetection()
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('yawn.jpg',0)
    img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    #cap = cv2.VideoCapture(0)
    #cap.set(3, 640)
    #cap.set(4, 480)
    #success, img = cap.read() 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.filter2D(img, -1, kernel=np.array([[0, -1, 0], [-1, 5.5, -1], [0, -1, 0]], np.float32))
    img = img[:, :]
    face = face_cascade.detectMultiScale(img, 1.1, 4)
    pro = process.process1()
    status = pro.process1(img)
    #gasleak check
    if(status == "Warning" or status == "Danger"):
        print("Calibration Done..")
        time.sleep(15)
        if(gascheck()):
            status = "SOS! GAS Leak"
    #display face
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, status, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    #cap.release()
    cv2.destroyAllWindows()
