from tkinter import *
from PIL import Image, ImageTk
import cv2

window = Tk()
window.title("Smart Parking Asistant")

#cap video
in_cap = cv2.VideoCapture(0)
out_cap = cv2.VideoCapture(1)

# Create a Label to capture the Video frames
frame_in = Label(window)
frame_in.grid(row=1, column=0)

frame_out = Label(window)
frame_out.grid(row=1, column=1)



def show_frame():
    #read image
    image1 = in_cap.read()[1]
    image2 = out_cap.read()[1]

    #cvt color
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image1 = Image.fromarray(image1)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    image2 = Image.fromarray(image2)

    # Convert image to PhotoImage

    imgtk1 = ImageTk.PhotoImage(image=image1)
    frame_in.imgtk1 = imgtk1
    frame_in.configure(image=imgtk1)

    imgtk2 = ImageTk.PhotoImage(image=image2)
    frame_out.imgtk2 = imgtk2
    frame_out.configure(image=imgtk2)

    # Repeat after an interval to capture continiously
    frame_out.after(20, show_frame)

    #show infor cam 1
    cin_plate = Label(window, text="Bien so xe: ", font=28).grid(row=2, column=0, sticky='w')
    cin_tikcet = Label(window, text="Ve xe: ", font=28).grid(row=3, column=0, sticky='w')

    #show infor cam 2
    cout_plate = Label(window, text="Bien so xe: ", font=28).grid(row=2, column=1, sticky='w')
    cout_ticket = Label(window, text="Ve xe: ", font=28).grid(row=3, column=1, sticky='w')


show_frame()

cam_1 = Label(window, text= "Camera cửa vào",font=32).grid(row=0, column=0)
cam_2 = Label(window, text= "Camera cửa ra",font=32).grid(row=0, column=1)



window.mainloop()