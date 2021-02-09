import cv2, dlib
import numpy as np
from imutils import face_utils
import math


class methods():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.eye_threshold = 0.2
        self.mouth_threshold = 0.1
        self.frame = None
        self.info = []

    # eye aspect ratio
    def eye_aspect_ratio(self, eye):
        A = np.sqrt((eye[1][0] - eye[5][0]) ** 2 + (eye[1][1] - eye[5][1]) ** 2)
        B = np.sqrt((eye[2][0] - eye[4][0]) ** 2 + (eye[2][1] - eye[4][1]) ** 2)
        C = np.sqrt((eye[0][0] - eye[3][0]) ** 2 + (eye[0][1] - eye[3][1]) ** 2)
        ear = (A + B) / (2.0 * C)
        return ear

    # gaze ratio
    def get_gaze_ratio(self, lmk):
        eye_region = np.array([(lmk[0].x, lmk[0].y),
                               (lmk[1].x, lmk[1].y),
                               (lmk[2].x, lmk[2].y),
                               (lmk[3].x, lmk[3].y),
                               (lmk[4].x, lmk[4].y),
                               (lmk[5].x, lmk[5].y)], np.int32)
        # cv.polylines(frame, [eye_region], True, (0, 0, 255), 2)
        height, width, _ = self.frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [eye_region], True, 255, 2)
        cv2.fillPoly(mask, [eye_region], 255)

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        eye = cv2.bitwise_and(gray, gray, mask=mask)

        min_x = max(0, np.min(eye_region[:, 0]))
        max_x = np.max(eye_region[:, 0])
        min_y = max(0, np.min(eye_region[:, 1]))
        max_y = np.max(eye_region[:, 1])

        gray_eye = eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 40, 255, cv2.THRESH_BINARY)
        h, w = threshold_eye.shape

        left_side_threshold = threshold_eye[0: h, 0: int(w / 2)]
        left_side_white = cv2.countNonZero(left_side_threshold)

        right_side_threshold = threshold_eye[0: h, int(w / 2): w]
        right_side_white = cv2.countNonZero(right_side_threshold)

        # print('left white:', left_side_white)
        # print('right white:', right_side_white)

        if left_side_white == 0 and right_side_white == 0:
            gaze_ratio = 1
        elif left_side_white == 0:
            gaze_ratio = 0.1
        elif right_side_white == 0:
            gaze_ratio = 10
        else:
            gaze_ratio = left_side_white / right_side_white
        return gaze_ratio

    # Drowsiness yawn gaze and headpose Detection
    def drowsiness(self, img, rect, dtype="int"):
        self.frame = img
        img = img[:, :, [2, 1, 0]]  # BGR => RGB
        yawn = False
        drowsiness = False
        landmarks = self.predictor(img, rect)

        # get the left and right eye coordinates
        left_eye = []
        for i in range(36, 42):
            left_eye.append([landmarks.part(i).x, landmarks.part(i).y])
        right_eye = []
        for i in range(42, 48):
            right_eye.append([landmarks.part(i).x, landmarks.part(i).y])

        #eye aspect ratio for both eyes
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)

        # average the eye aspect ratios
        ear = (left_ear + right_ear) / 2.0

        # print('ear:', ear, 'eye_threshold', self.eye_threshold)
        if ear < self.eye_threshold:
            drowsiness = True

        # check yawn
        top_lips = []
        bottom_lips = []
        for i in range(0, 68):
            if 50 <= i <= 53 or 61 <= i <= 64:
                top_lips.append((landmarks.part(i).x, landmarks.part(i).y))

            elif 65 <= i <= 68 or 56 <= i <= 59:
                bottom_lips.append((landmarks.part(i).x, landmarks.part(i).y))

        top_lips = np.squeeze(np.asarray(top_lips))
        bottom_lips = np.squeeze(np.asarray(bottom_lips))
        top_lips_mean = np.array(np.mean(top_lips, axis=0), dtype=dtype)
        bottom_lips_mean = np.array(np.mean(bottom_lips, axis=0), dtype=dtype)
        top_lips_mean = top_lips_mean.reshape(-1)
        bottom_lips_mean = bottom_lips_mean.reshape(-1)

        # distance=math.sqrt((bottom_lips_mean[0] - top_lips_mean[0])**2 + (bottom_lips_mean[-1] - top_lips_mean[-1])**2)
        distance = bottom_lips_mean[-1] - top_lips_mean[-1]

        threshold = (rect.bottom() - rect.top()) * self.mouth_threshold
        if distance > threshold:
            yawn = True

        # gaze detection
        left_gaze_ratio = self.get_gaze_ratio([landmarks.part(i) for i in range(36, 42)])
        right_gaze_ratio = self.get_gaze_ratio([landmarks.part(i) for i in range(42, 48)])
        gaze_ratio = (right_gaze_ratio + left_gaze_ratio) / 2
        if gaze_ratio <= 0.75:
            gaze = 'RIGHT'
        elif 0.75 < gaze_ratio < 1.3:
            gaze = 'CENTER'
        else:
            gaze = 'LEFT'

        # head pose detection
        shape0 = np.array(face_utils.shape_to_np(landmarks))
        image_points = np.array([
            (shape0[33, :]),  # Nose tip
            (shape0[8, :]),  # Chin
            (shape0[36, :]),  # Left eye left corner
            (shape0[45, :]),  # Right eye right corner
            (shape0[48, :]),  # Left Mouth corner
            (shape0[54, :])  # Right mouth corner
        ], dtype="double")

        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-225.0, 170.0, -135.0),  # Left eye left corner
            (225.0, 170.0, -135.0),  # Right eye right corne
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner
        ])

        focal_length = 640
        center = (320, 180)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        dist_coeffs = np.zeros((4, 1))
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                      dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector, camera_matrix, dist_coeffs)
        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        rvec_matrix = cv2.Rodrigues(rotation_vector)[0]

        proj_matrix = np.hstack((rvec_matrix, translation_vector))
        eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]

        pitch, yaw, roll = [math.radians(_) for _ in eulerAngles]

        pitch = math.degrees(math.asin(math.sin(pitch)))
        roll = -math.degrees(math.asin(math.sin(roll)))
        yaw = math.degrees(math.asin(math.sin(yaw)))

        return drowsiness, yawn, gaze, [p1, p2], [yaw, pitch * 4]

    def model(self, face, img):
        x1 = face.left()
        x2 = face.top()
        y1 = face.right()
        y2 = face.bottom()
        drowsiness1, yawn, gaze, head_pose, theta = self.drowsiness(img, face)
        info = [drowsiness1, yawn, gaze, x1, y1, x2, y2, head_pose, theta]
        return info
