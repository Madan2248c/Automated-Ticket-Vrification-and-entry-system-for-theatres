import qr_detector

class verification :

    def __init__(self) :
        self.qd = qr_detector.qr_detector()

    def start(self) :
        self.qd.start()

