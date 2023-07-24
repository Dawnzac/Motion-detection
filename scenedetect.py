import cv2 as md1
import cv2 as md2
import datetime
import ctypes
import winsound
from threading import Thread

duration = 1000
freq = 440
def img1():
    cap1 = md1.VideoCapture(0)

    mog = md1.createBackgroundSubtractorMOG2()
    c_count = 0

    while True:
        ret1, frame1 = cap1.read()
        gray = md1.cvtColor(frame1, md1.COLOR_BGR2GRAY)
        
        fgmask = mog.apply(gray)
        
        kernel = md1.getStructuringElement(md1.MORPH_ELLIPSE, (5, 5))
        fgmask = md1.erode(fgmask, kernel, iterations=1)
        fgmask = md1.dilate(fgmask, kernel, iterations=1)
        
        contours, hierarchy = md1.findContours(fgmask, md1.RETR_EXTERNAL, md1.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if md1.contourArea(contour) < 1000:
                continue
            
            x, y, w, h = md1.boundingRect(contour)
            md1.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            current_time = datetime.datetime.now()
            print ("Detected Change at " , current_time )
            c_count+= 1
            print (c_count)
            if c_count >= 2:
                winsound.MessageBeep()
                MB_SYSTEMMODAL = 0x00001000
                ctypes.windll.user32.MessageBoxW(0, "Scene Change Detected", "Alert", 1)
                break
        
        md1.imshow('Display Test', frame1)
        #final = md1.hconcat([frame1, frame2])
        if md1.waitKey(1000) == ord('q'):
            break 
    cap1.release()
    md1.destroyAllWindows()
    
def img2():
    cap2 = md2.VideoCapture(0)

    while True:
        ret2, frame2 = cap2.read()
        
        md2.imshow('Display Test Reference', frame2)
        #final = md1.hconcat([frame1, frame2])
        if md2.waitKey(1000) == ord('q'):
            break
        
    cap2.release()
    md2.destroyAllWindows()

#t1 = Thread(target=img1)
#t1.start()
t2 = Thread(target=img2)
t2.start()
