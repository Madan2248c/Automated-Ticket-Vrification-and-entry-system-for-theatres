import verification
from qr_detector import qr_detector

qrd1 = qr_detector()
qrd1.start()

if len(qrd1.output) > 0 :
    print(qrd1.output)

else :
    print("None")