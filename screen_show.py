
import cv2
from WPODNet_SVM.lib_detection import load_model, detect_lp, im2single
from WPODNet_SVM.read_plate import read_lisence
from QRCode.ScanQR import scan_qr
from threading import Thread

def detec_lisence(img):
    # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
    Dmax = 608
    Dmin = 288

    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(in_Frame.shape[:2])) / min(in_Frame.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)

    _, LpImg, lp_type = detect_lp(wpod_net, im2single(in_Frame), bound_dim, lp_threshold=0.9)
    lisence = "No lisence found"
    if (len(LpImg)):
        lisence = read_lisence(LpImg[0])
    print("bien so: ", lisence)

# Load model detection
wpod_net_path = "WPODNet_SVM/wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)


#video path
video_path = "WPODNet_SVM/test/test.MOV"

in_cap = cv2.VideoCapture(video_path)
out_cap = cv2.VideoCapture(0)
qr_cap = cv2.VideoCapture(0)

"""_, Frame = in_cap.read()

while not _:
    # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
    Dmax = 608
    Dmin = 288

    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(Frame.shape[:2])) / min(Frame.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)

    _, LpImg, lp_type = detect_lp(wpod_net, im2single(Frame), bound_dim, lp_threshold=0.9)

    if (len(LpImg)):
        lisence = read_lisence(LpImg[0])
        print(lisence)

    _, Frame = in_cap.read()"""


ret = 1
count = 0
data = ''

while ret:

    if count >= 5: count = 0

    ret, in_Frame = in_cap.read()
    ret, qr_Frame = qr_cap.read()
    #in_Frame = cv2.imread("WPODNet_SVM/test/541.jpg")
    data1 = scan_qr(qr_Frame)

    cv2.imshow("in_camera", in_Frame)
    cv2.imshow("qr camera", qr_Frame)
    cv2.waitKey(1)
    if data != data1:
        #count = 0
        data = data1

    if (data != '') & (count == 0):
        print("ma qr: ", data)
        thread = Thread(target= detec_lisence(in_Frame))
        thread.start()

    count = count + 1


    """if cv2.waitKey(10) & 0xFF == ord('q'):
        # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
        Dmax = 608
        Dmin = 288

        # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
        ratio = float(max(Frame.shape[:2])) / min(Frame.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)

        _, LpImg, lp_type = detect_lp(wpod_net, im2single(Frame), bound_dim, lp_threshold=0.9)
        if (len(LpImg)):
            lisence = read_lisence(LpImg[0])
            print(lisence)"""


