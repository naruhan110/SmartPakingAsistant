import tkinter
from tkinter import *
import cv2
from WPODNet_SVM.lib_detection import load_model, detect_lp, im2single
from WPODNet_SVM.read_plate import read_lisence
from QRCode.ScanQR import scan_qr
from threading import Thread
from data import *
from tkinter_camera import *

sources =[
    ('Camera cua vao', 1),
    ('camera cua ra', 0)
]
smartparking = Tk()
#smartparking.title("Smart Parking")
# Create a window and show 2 camera
App(smartparking, "Smart Paking", sources)
