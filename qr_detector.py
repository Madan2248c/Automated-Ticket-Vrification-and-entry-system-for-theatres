#qr_detector.py

import cv2

class qr_detector : 
    def __init__(self):
        self.output = ""
        self.camera_id = 0
        self.delay = 1
        self.window_name = "QR Detector"

        self.qcd = cv2.QRCodeDetector()
        # self.cap = cv2.VideoCapture(self.camera_id)
    
    def start(self) :
        while True :
            ret,frame = self.cap.read()

            if ret :
                ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
                if ret_qr:
                    for s, p in zip(decoded_info, points):
                        if s:
                            self.output = s
                            color = (0, 255, 0)
                        else:
                            color = (0, 0, 255)
                        frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
                cv2.imshow(self.window_name, frame)

            if (cv2.waitKey(self.delay) & 0xFF == ord('q')) or (len(self.output) > 0):
                break

        cv2.destroyWindow(self.window_name)

    def detectfromaframe(self,frame):
        ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    self.output = s
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        return frame
    