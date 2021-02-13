import cv2, dlib
import numpy as np
import os
from queue import Queue
from method import methods


class process1():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.max_frame_count = int(os.getenv('MAX_FRAME_COUNT', 0))
        self.frame_count = self.max_frame_count
        self.head_vote = [Queue(15) for _ in range(5)]  # down, left_more, right_more, left_less, right_less
        self.head_sum = [0, 0, 0, 0, 0]
        for i in range(5):
            for _ in range(15):
                self.head_vote[i].put(False)
    def process1(self,img):
        # Process
        faces = self.detector(img)
        face = None
        area = 0
        for i in faces:
            face_area = (i.right() - i.left() + 1) * (i.bottom() - i.top() + 1)
            if face_area > area:
                face = i
                area = face_area
        # print(face)
        # ---------------------------------------------------------------------------------------------------------------
        if face is not None:
            image: np.ndarray = img
            mod = methods()
            if self.frame_count >= self.max_frame_count:
                info = mod.model(face, image)
                self.frame_count = 0
            else:
                self.frame_count += 1

            drowsiness, yawn, gaze, x1, y1, x2, y2, head_pose, theta = info

            if drowsiness == True and yawn == True:
                safety_status = 'Danger'
            elif drowsiness == True or yawn == True:
                safety_status = 'Warning'
            else:
                safety_status = 'Safe'

            # head pose status
            tmp = [False] * 5
            if theta[1] < -20:
                tmp[0] = True
            if theta[0] > 20:
                tmp[1] = True
            elif theta[0] > 10:
                tmp[3] = True
            if theta[0] < -35:
                tmp[2] = True
            elif theta[0] < -20:
                tmp[4] = True

            for i in range(5):
                self.head_sum[i] += tmp[i]
                self.head_sum[i] -= self.head_vote[i].get()
                self.head_vote[i].put(tmp[i])

            self.headpose_status = 5
            for i, s in enumerate(self.head_sum):
                if s > 10:
                    self.headpose_status = i
                    break

            print("|" + "drowsiness: " + str(drowsiness) + " |" + "yawn: " + str(yawn) + " |" + "gaze: " + str(
                gaze) + " |" + "safety_status: " + str(safety_status) + " |" + "headpose_status: " + str(
                self.headpose_status))
            
            #returning status of the person
            return(safety_status)
                
            return("|" + "drowsiness: " + str(drowsiness) + " |" + "yawn: " + str(yawn) + " |" + "gaze: " + str(
                gaze) + " |" + "safety_status: " + str(safety_status) + " |" + "headpose_status: " + str(
                self.headpose_status))
