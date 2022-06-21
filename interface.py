


# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
from WPODNet_SVM.lib_detection import load_model, detect_lp, im2single
from WPODNet_SVM.read_plate import read_lisence, detec_plate
from QRCode.ScanQR import scan_qr
from threading import Thread

def detec_lisence(Frame):

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


# Load model detection
wpod_net_path = "WPODNet_SVM/wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)


# Create an instance of TKinter Window or frame
win = Tk()

"""# Set the size of the window
win.geometry("1000x750")"""

# Create a Label to capture the Video frames
label = Label(win)
label.grid(row=0, column=0)
in_cap = cv2.VideoCapture(1)
qr_cap = cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
   # Get the latest frame
   ret, in_Frame = in_cap.read()

   img = cv2.cvtColor(in_Frame, cv2.COLOR_BGR2RGB)
   img = Image.fromarray(img)

   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)

   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

   #read qr
   qr_Frame = qr_cap.read()[1]
   data = scan_qr(qr_Frame)

   if data!= '':
      print("ma qr: ", data)
      thread = Thread(target=detect_plate, args=(in_Frame,))
      #thread = Thread(target = dung_dinh(30))
      thread.start()
      thread.join()
   Label1 = Label(win, text='Biển số xe :', font=("Arial", 30)).grid(row=100, column=0)
   Label1 = Label(win, text='Thời điểm xe vào :', font=("Arial", 30)).grid(row=101, column=0)
   Label1 = Label(win, text='Thời điểm xe ra :', font=("Arial", 30)).grid(row=102, column=0)
   Label2 = Label(win, text='Phí:', font=("Arial", 30)).grid(row=103, column=0)


show_frames()
win.mainloop()
