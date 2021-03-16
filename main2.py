import cv2
import numpy as np
import process
import time
from calibration.gas_detection import GasDetection

def gascheck():
    detection = GasDetection()
    print("Calibration Done..")
    time.sleep(3)
    print("Start Gas")
    time.sleep(15)
    ppm = detection.percentage()
    mean = (ppm[detection.CO_GAS] + ppm[detection.CH4_GAS] + ppm[detection.LPG_GAS] + ppm[detection.PROPANE_GAS] + ppm[detection.ALCOHOL_GAS]) / 5
    print(mean)
    if(mean>1):
        return True
    else:
        return False

def ddd():
    print("Calibrating Sensor..")
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('d.jpg',0)
    img = cv2.resize(img, (0, 0), fx = 1, fy = 1)
    #cap = cv2.VideoCapture(0)
    #cap.set(3, 640)
    #cap.set(4, 480)
    #success, img = cap.read() 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.filter2D(img, -1, kernel=np.array([[0, -1, 0], [-1, 5.5, -1], [0, -1, 0]], np.float32))
    img = img[:, :]
    face = face_cascade.detectMultiScale(img, 1.1, 4)
    pro = process.process1()
    status, detail = pro.process1(img)
    #gasleak check
    if(status == "Warning" or status == "Danger"):
        if(gascheck()):
            status = "SOS! GAS Leak"
    #display face
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if status is not "Safe":
            cv2.putText(img, status, (x, y-10), cv2.FONT_HERSHEY_TRIPLEX, 4, (0,0,255), 7)
        else:
            cv2.putText(img, status, (x, y-10), cv2.FONT_HERSHEY_TRIPLEX, 4, (36,255,12), 7)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    #cap.release()
    cv2.destroyAllWindows()
    return status,img

if __name__ == '__main__':
    ddd()
