
# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import cv2
import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
import cv2


mydb = mysql.connector.connect(
   host='127.0.0.1',
   user='root',
   password='nhan1691999',
   port='3306',
   database='test11'
)

mydb2 = mysql.connector.connect(
   host='127.0.0.1',
   user='root',
   password='nhan1691999',
   port='3306',
   database='test12'
)

def update(rows):
   for i in rows:
      trv.insert('','end',values = i)
result = ""
def search11():
   bienso = e1.get()
   x = []
   mycursor2.execute("SELECT THOI_GIAN_VAO FROM xe_trong_baii WHERE bien_so_xe = '" + bienso + "'")
   result = mycursor2.fetchall()


   e2.delete(0, END)
   e2.insert(END, x)

mycursor2 = mydb2.cursor()
stt2 = "SELECT STT FROM test12.xe_trong_baii"
mycursor2.execute(stt2)
mystt2 = mycursor2.fetchall()

mycursor = mydb.cursor()
stt = "SELECT STT FROM test11.bien_so_xe"
mycursor.execute(stt)
mystt = mycursor.fetchall()

bsx = "SELECT BIEN_SO FROM test11.bien_so_xe"
mycursor.execute(bsx)
mybsx = mycursor.fetchall()
tgv = "SELECT THOIGIAN_VAO FROM test11.bien_so_xe"
mycursor.execute(tgv)
mytgv = mycursor.fetchall()
tgr = "SELECT THOIGIAN_RA FROM test11.bien_so_xe"
mycursor.execute(tgr)
mytgr = mycursor.fetchall()


win = Tk()
# Set the size of the window
win.geometry("1000x750")
win.configure(bg='lavender')

trv = ttk.Treeview(win,columns=(1,2,3),show="headings",height="6")
trv.grid(row = 11,column = 0)
trv.heading(1,text="STT")
trv.heading(2,text="Biển số xe")
trv.heading(3,text="Thời gian vào")
rows = mycursor2.fetchall()


query = "SELECT STT,bien_so_xe,THOI_GIAN_VAO from xe_trong_baii"
mycursor2.execute(query)
rows = mycursor2.fetchall()
update(rows)
# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=6,column =0,sticky = W+N)
cap= cv2.VideoCapture(0)
cap.set(3,300)
cap.set(4,200)
# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

show_frames()

varb = StringVar()
var = StringVar()
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()

Label1 = Label(win,text ="Stt:",font=("Arial", 10 )).grid(row = 0,column = 0,sticky=W+N)
Label1 = Label(win,textvariable=var ,font=("Arial", 10 )).grid(row = 0,column = 0)
var.set(mystt)
Label1 = Label(win, text = 'Biển số xe :',font=("Arial", 10 )).grid(row = 1,column = 0,sticky=W+N)
Label1 = Label(win,textvariable=var1 ,font=("Arial", 10 )).grid(row = 1,column=0)
var1.set(mybsx)
Label1 = Label(win, text = 'Thời điểm xe vào :',font= ("Arial", 10)).grid(row = 2,column = 0,sticky=W+N)
Label1 = Label(win,textvariable=var2 ,font=("Arial", 10 )).grid(row = 2,column=0)
var2.set(mytgv)
Label1 = Label(win, text = 'Thời điểm xe ra :',font= ("Arial", 10)).grid(row = 3,column = 0,sticky=W+N)
Label1 = Label(win,textvariable=var3 ,font=("Arial", 10 )).grid(row = 3,column=0)
var3.set(mytgr)
Labelp = Label(win, text = 'Phí:',font= ("Arial", 10)).grid(row=4,column=0,sticky=W+N)
mybutton1 = Button(win, text = 'Doanh thu trong ngày:',font= ("Arial", 10)).grid(row=5,column=0,sticky=W+N)
Labelb = Label(win, text = 'DANH SÁCH XE HIỆN ĐANG TRONG BÃI ',font= ("Arial", 25)).grid(row=10,column=0,sticky=W)
Labell = Label(win, text = 'TÌM KIẾM XE TRONG BÃI NGÀY HÔM NAY ',font= ("Arial", 25)).grid(row=12,column=0,sticky=W)
Labelll = Label(win,text = 'Nhập số xe',font= ("Arial", 10)).grid(row = 13,column = 0,sticky=W)
e1=Entry(win)
e1.grid(row = 14,column = 0)
e2=Entry(win)
e2.grid(row = 15,column = 0)
bienso = ""
Btn = Button(win,text = 'Tìm kiếm', command = search11())
Btn.grid(row = 14,column=0,sticky=W)
Labelll = Label(win,text = 'Thời gian xe vào:',font= ("Arial", 10)).grid(row = 15,column = 0,sticky=W)

win.mainloop()
