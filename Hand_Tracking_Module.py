import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import time


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime = 0
Ctime = 0


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
v_Range = volume.GetVolumeRange()


MinVol = v_Range[0]
MaxVol = v_Range[1]

while True:
    success, img= cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    lmList = []
    if result.multi_hand_landmarks:
        for handLns in result.multi_hand_landmarks:
            for id,ln in enumerate (handLns.landmark):
                h, w, c = img.shape
                cx, cy = int(ln.x*w), int(ln.y*h)
                lmList.append([id, cx, cy])

            mpDraw.draw_landmarks(img, handLns, mpHands.HAND_CONNECTIONS)


    if lmList !=[]:
        a1 , b1 = lmList[4][1], lmList[4][2]
        a2 , b2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (a1,b1), 10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (a2, b2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (a1, b1), (a2, b2), (255, 0, 0), 3)

        length = math.hypot(a2 - a1, b2 - b1)
        #print(length)

        vol = np.interp(length, [15, 220], [MinVol, MaxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


    Ctime = time.time()
    fps = 1 / (Ctime - ptime)
    ptime = Ctime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)

    cv2.imshow("Capture",img)
    cv2.waitKey(1)
