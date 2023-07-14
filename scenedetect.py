import cv2
import datetime
import ctypes

current_time = datetime.datetime.now()

cap1 = cv2.VideoCapture(0)

mog = cv2.createBackgroundSubtractorMOG2()

cap2 = cv2.VideoCapture(0)


while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    fgmask = mog.apply(gray)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print ("Detected Change at " , current_time )
        ctypes.windll.user32.MessageBoxW(0, "Scene Change Detected", "Alert", 1)
    
    cv2.imshow('Display Test', frame2)
    #cv2.imshow('Display Test Reference', frame1)
    #final = cv2.hconcat([frame1, frame2])
    #cv2.imshow("Display Test", final)
    if cv2.waitKey(1) == ord('q'):
        break
    
        
cap1.release()
cap2.release()
cv2.destroyAllWindows()
