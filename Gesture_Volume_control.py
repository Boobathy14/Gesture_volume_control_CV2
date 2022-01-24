import cv2
import time
import numpy as np

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime = 0
while True:
    success, img= cap.read()

    Ctime = time.time()
    fps = 1/(Ctime-ptime)
    ptime = Ctime

    cv2.putText(img,f'FPS:{int (fps)}',(48,50),cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,255),3)

    cv2.imshow('Img', img)
    cv2.waitKey(1)