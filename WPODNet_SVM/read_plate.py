import cv2
import numpy as np
from WPODNet_SVM.lib_detection import load_model, detect_lp, im2single
from threading import Thread


# Ham sap xep contour tu trai sang phai
def sort_contours(cnts):

    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts



# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    char_list = '0123456789ABCDEFGHKLMNPRSTUVXYZ'
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString


# Load model LP detection
wpod_net_path = "WPODNet_SVM/wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)


"""
Frame = cv2.imread("test/541.jpg")

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288

# Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
ratio = float(max(Frame.shape[:2])) / min(Frame.shape[:2])
side = int(ratio * Dmin)
bound_dim = min(side, Dmax)

_ , LpImg, lp_type = detect_lp(wpod_net, im2single(Frame), bound_dim, lp_threshold=0.9)"""

def read_lisence(LpImg, digit_w = 30, digit_h = 60):

    model_svm = cv2.ml.SVM_load('WPODNet_SVM/svm.xml')

    # Chuyen doi anh bien so
    LpImg = cv2.convertScaleAbs(LpImg, alpha=(255.0))

    roi = LpImg

    # Chuyen anh bien so ve gray
    gray = cv2.cvtColor( LpImg, cv2.COLOR_BGR2GRAY)


    # Ap dung threshold de phan tach so va nen
    binary = cv2.threshold(gray, 127, 255,
                         cv2.THRESH_BINARY_INV)[1]

    """cv2.imshow("Anh bien so sau threshold", binary)
    cv2.waitKey()"""

    # Segment kí tự
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
    cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    plate_info = ""

    for c in sort_contours(cont):
        (x, y, w, h) = cv2.boundingRect(c)
        ratio = h/w
        if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
            if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len

                # Ve khung chu nhat quanh so
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Tach so va predict
                curr_num = thre_mor[y:y+h,x:x+w]
                curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                _, curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)
                curr_num = np.array(curr_num,dtype=np.float32)
                curr_num = curr_num.reshape(-1, digit_w * digit_h)

                # Dua vao model SVM
                result = model_svm.predict(curr_num)[1]
                result = int(result[0, 0])

                if result<=9: # Neu la so thi hien thi luon
                    result = str(result)
                else: #Neu la chu thi chuyen bang ASCII
                    result = chr(result)

                plate_info +=result

    return plate_info

def detec_plate(Frame):

    # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
    Dmax = 500
    Dmin = 374

    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(Frame.shape[:2])) / min(Frame.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)

    _, LpImg, lp_type = detect_lp(wpod_net, im2single(Frame), bound_dim, lp_threshold=0.9)
    lisence = "No lisence found"
    if (len(LpImg)):
        process_plate = Thread(target=read_lisence, args=(LpImg[0],))
        lisence = process_plate.start()
        process_plate.join()
    print("bien so: ", lisence)


    """cv2.imshow("Cac contour tim duoc", roi)
    cv2.waitKey()"""

    """# Viet bien so len anh
    cv2.putText(Frame,fine_tune(plate_info),(50, 50), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), lineType=cv2.LINE_AA)"""

    """# Hien thi anh
    if 5 < len(plate_info) < 10:
        print("Bien so=", plate_info)
        cv2.imshow("Hinh anh output",Frame)
        cv2.imshow("Cac contour tim duoc", roi)
        cv2.imshow("Anh bien so sau threshold", binary)
        cv2.waitKey()"""

#cv2.destroyAllWindows()

"""print(read_lisence(LpImg[0]))"""
