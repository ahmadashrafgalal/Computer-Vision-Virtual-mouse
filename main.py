import cv2
import numpy as np
import HandTrackingModule as htm
import time 
import pyautogui

cap = cv2.VideoCapture(0)
cam_width, cam_height = 640, 480
cap.set(3, cam_width)
cap.set(4, cam_height)
Screen_width, Screen_height = pyautogui.size()
frameR = 150 
smothing = 7
Previous_locX, Previous_locY = 0, 0
Current_locX, Current_locY = 0, 0

detector = htm.handDetector(maxHands=1)

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    cv2.rectangle(img, (frameR,frameR), (cam_width - frameR, cam_height - frameR), (255, 0, 255), 2)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        fingers = detector.fingersUp()

        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, cam_width-frameR), (0, Screen_width))
            y3 = np.interp(y1, (frameR, cam_height-frameR), (0, Screen_height))
            Current_locX = Previous_locX + (x3 - Previous_locX) / smothing
            Current_locY = Previous_locY + (y3 - Previous_locY) / smothing
            pyautogui.moveTo(Screen_width - Current_locX, Current_locY) 
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            Previous_locX, Previous_locY = Current_locX, Current_locY

        if fingers[1] == 1 and fingers[2] == 1:
            lengh, img, lineinfo = detector.findDistance(8, 12, img)
            if lengh < 35:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                pyautogui.click()
                time.sleep(0.2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)