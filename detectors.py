#qr_detector.py

import time
import cv2
import mediapipe as mp

class QrDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.qcd = cv2.QRCodeDetector()
        self.output = ""
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.prev_right_ear_x = 0
        self.crossing_count = 0
        self.newframe1 = None
        self.output1 = None


    def detect_from_a_frame(self):
        ret, frame = self.cap.read()
        ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)

        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    self.output = s
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)

        return frame, self.output
    
    def detector(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)

        middle_x = image.shape[1] // 2
        image_copy = image.copy()
        cv2.line(image_copy, (middle_x, 0), (middle_x, image.shape[0]), (0, 255, 0), 2)
        image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

        if results.pose_landmarks:
            right_ear_landmark = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_EAR]
            if right_ear_landmark.visibility > 0.5:
                right_ear_x, right_ear_y = int(right_ear_landmark.x * image.shape[1]), int(right_ear_landmark.y * image.shape[0])

                image_copy = image.copy()
                cv2.circle(image_copy, (right_ear_x, right_ear_y), 8, (0, 0, 255), -1)
                image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

                if right_ear_x < middle_x and self.prev_right_ear_x >= middle_x:
                    self.crossing_count += 1

                self.prev_right_ear_x = right_ear_x

        image.flags.writeable = True
        cv2.putText(image, f"Crossings: {self.crossing_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return image, self.crossing_count
    
    def count_persons_in10sec(self,start_time):
        cmp = 0
        while time.time() - start_time < 3 :
            self.newframe1, self.output1 = self.detector()
            return self.newframe1,self.output1,cmp
        cmp = 1
        return self.newframe1,self.output1,cmp