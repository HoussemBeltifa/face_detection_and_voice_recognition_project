import tkinter as tk
import cv2
import os
import numpy as np
from utils import CFEVideoConf, image_resize

try:
    from googlesearch import *
except ImportError:
    print("No module named 'google' found")


def test():
    import speech_recognition as sr

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    # recognize speech using Google Speech Recognition
    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    finally:
        pass
     
    # search
    query =  str(r.recognize_google(audio))
 
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(j)

    import webbrowser

    
    chrome_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chrome.exe %s'
    for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
        webbrowser.open("https://google.com/search?q=%s" % query)

def face():
    
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)


    while True:
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    # Release the VideoCapture object
    cap.release()

def faceRecord():

    cap = cv2.VideoCapture(0)
    ch='Videos/video'
    save_path = 'Videos/video.avi'
    frames_per_seconds = 24.0
    config = CFEVideoConf(cap, filepath=save_path, res='720p')
    out = cv2.VideoWriter(save_path, config.video_type, frames_per_seconds, config.dims)


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        out.write(frame)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def Like_A_Boss():
    cap = cv2.VideoCapture(0)

    save_path           = 'videos/glasses_and_stash.mp4'
    frames_per_seconds  = 24
    config              = CFEVideoConf(cap, filepath=save_path, res='720p')
    out                 = cv2.VideoWriter(save_path, config.video_type, frames_per_seconds, config.dims)
    face_cascade        = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
    eyes_cascade        = cv2.CascadeClassifier('cascades/third-party/frontalEyes35x16.xml')
    nose_cascade        = cv2.CascadeClassifier('cascades/third-party/Nose18x15.xml')
    glasses             = cv2.imread("images/fun/glasses.png", -1)
    mustache            = cv2.imread('images/fun/mustache.png',-1)


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray            = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces           = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        for (x, y, w, h) in faces:
            roi_gray    = gray[y:y+h, x:x+h] 
            roi_color   = frame[y:y+h, x:x+h]

            eyes = eyes_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=5)
            for (ex, ey, ew, eh) in eyes:
                roi_eyes = roi_gray[ey: ey + eh, ex: ex + ew]
                glasses2 = image_resize(glasses.copy(), width=ew)

                gw, gh, gc = glasses2.shape
                for i in range(0, gw):
                    for j in range(0, gh):
                        if glasses2[i, j][3] != 0: 
                            roi_color[ey + i, ex + j] = glasses2[i, j]


            nose = nose_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=5)
            for (nx, ny, nw, nh) in nose:
                roi_nose = roi_gray[ny: ny + nh, nx: nx + nw]
                mustache2 = image_resize(mustache.copy(), width=nw)

                mw, mh, mc = mustache2.shape
                for i in range(0, mw):
                    for j in range(0, mh):
                        
                        if mustache2[i, j][3] != 0: 
                            roi_color[ny + int(nh/2.0) + i, nx + j] = mustache2[i, j]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


    
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

button = tk.Button(frame, 
                   text="Face detection\n(press ECS \nto stop)", 
                   fg="white",bg='#293241',
                   command=face,height= 5, width=10)
button.pack(side=tk.LEFT)

button = tk.Button(frame, 
                   text="Record Video\npress Q to exit", 
                   fg="yellow",bg='#3D5A80',
                   command=faceRecord,height= 5, width=10)
button.pack(side=tk.LEFT)
button = tk.Button(frame, 
                   text="Video for fun\npress Q to exit", 
                   fg="red",bg='#98C1D9',
                   command=Like_A_Boss,height= 5, width=10)
button.pack(side=tk.LEFT)

slogan = tk.Button(frame,
                   text="Need some\n help?",bg='#AEF359',
                   command=test,height= 5, width=10)
slogan.pack(side=tk.LEFT)

button = tk.Button(frame, 
                   text="QUIT", borderwidth=4, relief="solid",
                   fg="black",bg='#EE6C4D',
                   command=quit,height= 5, width=10)
button.pack(side=tk.LEFT)
#button.place(x=100, y=50)


root.configure(bg='#E0FBFC')
root.title('face detection and voice recognize')
root.geometry("700x500")
root.mainloop()


