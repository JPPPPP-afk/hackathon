from tkinter import *
from tkinter import PhotoImage, messagebox
import tkinter
from PIL import ImageTk, Image
import recorder
from speech_to_text import speech_to_text
import os,sys

def start():
    global running

    if running is not None:
        print('already running')
    else:
        running = rec.open('Audio/temp.wav', 'wb')
        running.start_recording()

def stop():
    global running

    if running is not None:
        running.stop_recording()
        running.close()
        running = None
        speech_to_text(inputfile='Audio/temp.wav', outputfile='Audio/temp_result.txt')
        with open('Audio/temp_result.txt') as f:
            contents = f.read()
        lb = Message(root, 
                text=contents
                )
        lb.pack()
    else:
        print('not running')
# --- main ---

rec = recorder.Recorder(channels=2)
running = None

root = Tk()
root.geometry("600x700+400+80")
root.resizable(False,False)
root.title("Voice Recorder")
root.configure(background="#4a4a4a")

img=Image.open('mic.png')
img = ImageTk.PhotoImage(img)
root.iconphoto(False, img)
imgBg = Label(image=img, background="#4a4a4a" )
imgBg.pack(padx=5,pady=5)

frame = LabelFrame(root, height=50, width = 75)
frame.pack()

button_rec = Button(frame, font="arial 20", text='Start', command=start)
button_rec.grid(row=0, column=0)

button_stop = Button(frame, font="arial 20", text='Stop', command=stop)
button_stop.grid(row=0,column=1)

root.mainloop() 