from ttkthemes import themed_tk as tk
from tkinter import *
from tkinter.ttk import *
import win32com.client as wincl
from pyautogui import typewrite,hotkey
import time
from sys import exit
import os
import PIL.Image
from PIL import ImageTk,ImageGrab,ImageOps
import numpy as np
import keras
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
config = tf.ConfigProto(intra_op_parallelism_threads=4,\
        inter_op_parallelism_threads=4, allow_soft_placement=True,\
        device_count = { 'GPU' : 0})
session = tf.Session(config=config)
K.set_session(session)

model = Sequential()
model.add(Conv2D(128, kernel_size=(5, 5),
                 activation='relu',
                 input_shape=(28,28,1)))
model.add(Conv2D(256, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(63, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
model.load_weights("digrecer.h5")
root=tk.ThemedTk()
canvas_width = 500
canvas_height = 200
im=None
def goback():
    session.close() 
    root.destroy()
    os.system('python welcome.py')
    exit(0)
def getter(widget):
    label2['text']=''
    label['text']=''
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    img=ImageGrab.grab().crop((x,y,x1,y1))
    img=separate(img)
    xs=[]
    for im in img:
        try:
            im = im.convert('L')
            im.resize((28,28),PIL.Image.ANTIALIAS)
            im.thumbnail((28,28),PIL.Image.ANTIALIAS)
            im.point(lambda x: 0 if x<128 else 255, '1')
            im=np.array(im)
            im=np.swapaxes(im,0,1)
            im=PIL.Image.fromarray(im)
            im=np.array(im)
            im=im.reshape(1,28, 28,1)
            im=im.astype('float32')
            im /= 255
            xs.append(im)
        except:
           label2["text"]="some of the things you wrote\nare to small"
    xs=np.array(xs)
    xs=xs.reshape(xs.shape[0],28, 28,1)
    print(model.predict(xs))
    predict=np.argmax(model.predict(xs),1)
    for i in predict:
        if i>9:
            if i>35:
                
                if i==62:
                    i=" "
                else:
                    i=chr(i+61)
            else:
                i=chr(i+55)
        label['text']+=str(i)
def separate(im):
    im=im.convert('L')
    im = ImageOps.invert(im)
    im=im.convert('1')
    im=im.convert('L')
    im=np.array(im).astype(int)
    im=np.swapaxes(im,0,1)
    pics=[]
    places=[]
    num=False
    for i in range(len(im)):
        z=np.zeros(len(im[i]))
        if(not np.array_equal(im[i],z) and not num):
            places.append(i-1)
            num=True
        if(np.array_equal(im[i],z) and num):
            places.append(i+1)
            num=False
        if(len(places)==2):
            pics.append(places)
            places=[]
    images=[]
    for i in pics:
        try:
            img=np.array(im[i[0]:i[1]]).astype(int)
            img=np.swapaxes(img,0,1)
            height0=None
            height1=None
            for j in range(len(img)):
                z=np.zeros(len(img[j]))
                if(not np.array_equal(img[j],z)):
                    height0=j-1
                    break
            for j in range(len(img)):
                if(not np.array_equal(img[-j],z)):
                    height1=len(img)-j-1
                    break
            img=np.array(img[height0:height1]).astype(int)
            img=PIL.Image.fromarray(img)
            img=img.convert('L')
            img.thumbnail(img.size,PIL.Image.ANTIALIAS)
            images.append(img)
        except:
            label2["text"]="some of the things you wrote\nare to small"
    pics=[]
    for pic in images:
        pic=np.array(pic)
        pic=pic.tolist()
        while len(pic[0])>len(pic):
            pic.append(np.zeros(len(pic[0])))
            if len(pic[0])>len(pic):
                pic[0:0] = [np.zeros(len(pic[0]))]
        pic=np.swapaxes(np.array(pic),0,1)
        pic=pic.tolist()
        while len(pic[0])>len(pic):
            pic.append(np.zeros(len(pic[0])))
            if len(pic[0])>len(pic):
                pic[0:0] = [np.zeros(len(pic[0]))]
        pic=np.swapaxes(np.array(pic),0,1)
        pic=PIL.Image.fromarray(pic)
        pic=pic.convert('L')
        pic.thumbnail(pic.size,PIL.Image.ANTIALIAS)
        pics.append(pic)

        
    return pics
def typew(w):
    getter(w)
    hotkey('alt','tab')
    typewrite(label["text"])
def typewtxt():
    hotkey('alt','tab')
    with open("save.txt", "r") as myfile:
        typewrite(str(myfile.read()))

def read(w):
    getter(w)
    s=wincl.Dispatch("SAPI.SpVoice")
    s.Speak(label["text"])
def readtxt():
    s=wincl.Dispatch("SAPI.SpVoice")
    with open("save.txt", "r") as myfile:
        s.Speak(str(myfile.read()))
def backspace():
    with open("save.txt", 'rb+') as myfile:
        myfile.seek(-1, os.SEEK_END)
        myfile.truncate()
    with open("save.txt", "r") as myfile:
        txt["text"]=str(myfile.read())
def endsentence():
    with open("save.txt", "a") as myfile:
        myfile.write(".")
    with open("save.txt", "r") as myfile:
        txt["text"]=str(myfile.read())
def enter():
    with open("save.txt", "a") as myfile:
        myfile.write("\n")
    with open("save.txt", "r") as myfile:
        txt["text"]=str(myfile.read())
def write(w):
    getter(w)
    with open("save.txt", "a") as myfile:
        myfile.write(label["text"])
    with open("save.txt", "r") as myfile:
        txt["text"]=str(myfile.read())
def clear():
    label2['text']=''
    can.delete("all")
    label['text']=''
def txtclear():
    open("save.txt","w").close()
    with open("save.txt", "r") as myfile:
        txt["text"]=str(myfile.read())
def paint( event ):
    global color
    global paintsize
    x1, y1 = ( event.x - paintsize), ( event.y - paintsize )
    x2, y2 = ( event.x + paintsize), ( event.y + paintsize )
    w.create_oval( x1, y1, x2, y2, fill = color, outline="" )
def eracer():
    global color 
    color="#ffffff"
    global paintsize
    paintsize=10
def pen():
    global color 
    color="#000000"
    global paintsize
    paintsize=5
global paintsize
paintsize=5
global color
color="#000000"
w = Canvas(root, 
           width=canvas_width, 
           height=canvas_height)
w['bg']="#ffffff"
w.bind( "<B1-Motion>", paint )
w.pack(fill=X)
can=w
s =Style()
s.theme_use('plastik')
s.configure('my.THead', font=("Courier", 33,"bold"))
s.configure('my.TButton', font=("Courier", 33)) 
s.configure('my.TLabel', font=("Courier", 33))
s.configure('m.TLabel', font=("Courier", 33,"bold"))
t=Label(root,text="canvas manipulation", style='m.TLabel')
t.pack(pady=10)
cm=Frame(root)
cm.pack(pady=10)
txtm=Frame(root)


b=Button(cm,text="clear",command=lambda:clear(), style='my.TButton')
b.grid(row=0,column=1)
c=Button(cm,text="predict",command=lambda:getter(w), style='my.TButton')
c.grid(row=0,column=2)
d=Button(cm,text="save",command=lambda:write(w), style='my.TButton')
d.grid(row=0,column=3)
b=Button(txtm,text="clear",command=lambda:txtclear(), style='my.TButton')
b.grid(row=0,column=2)
d=Button(txtm,text="add .",command=lambda:endsentence(), style='my.TButton')
d.grid(row=0,column=3)
d=Button(txtm,text="enter",command=lambda:enter(), style='my.TButton')
d.grid(row=0,column=4)
c=Button(txtm,text="say",command=lambda:readtxt(), style='my.TButton')
c.grid(row=0,column=6)
c=Button(txtm,text="backspace",command=lambda:backspace(), style='my.TButton')
c.grid(row=0,column=5)
c=Button(txtm,text="type",command=lambda:typewtxt(), style='my.TButton')
c.grid(row=0,column=7)
delete=Button(cm,text="eraser",command=lambda:eracer(), style='my.TButton')
delete.grid(row=0,column=4)
pencil=Button(cm,text="pen",command=lambda:pen(), style='my.TButton')
pencil.grid(row=0,column=5)
c=Button(cm,text="say",command=lambda:read(w), style='my.TButton')
c.grid(row=0,column=6)
c=Button(cm,text="type",command=lambda:typew(w), style='my.TButton')
c.grid(row=0,column=7)
label=Label(root,text="", style='my.TLabel')
label.pack(pady=50)
t=Label(root,text="text file manipulation", style='m.TLabel')
t.pack(pady=10)

txtm.pack(pady=10)

with open("save.txt", "r") as myfile:
        txt=Label(root,text=str(myfile.read()),style='my.TLabel')
txt.pack(pady=50)
label2=Label(root,text="", style='my.TLabel')
label2.pack(pady=50)
root.mainloop()
