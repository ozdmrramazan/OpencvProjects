"""
Parking_Space_Detection kodunda yerleştirdiğimiz alanların dolu olup olmadığının tespitini yapacağız
Bunun ince ayarlamasını da parametreler olan threshold, weight ve height ile yapacağız
"""

import cv2 
import pickle
import numpy as np


cap = cv2.VideoCapture('video.mp4')
width = 25
height = 13
# pickle ettiğimiz dosyayı import ediyoruz
with open('CarParkPos', 'rb') as p:
    posList = pickle.load(p)


def CheckParkSpace(img_):
    space_counter = 0
    
    for pos in posList:
        x, y = pos
        
        img_crop = img_[y: y + height, x: x + width]
        count = cv2.countNonZero(img_crop)
        
        print('count: ', count)
        # burada arabanın çerçeve içerisindeki değerine göre check işlemi yapıyoruz
        if count < 145:
            color = (0, 255, 0)
            thickness = 2
            space_counter +=1
        else:
            color = (0, 0, 255)
            thickness = 2
        # burada da çerçeve içerisindeki miktarının değerini ekrana yazdırıyoruz   
        cv2.rectangle(img, pos, (x + width, y + height), color, thickness)
        cv2.putText(img, str(count), (x,y+height-1), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
        
    cv2.putText(img, F'Free: {space_counter}/{len(posList)}', (15,24), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 1)
            
while True:
    ret, img = cap.read()
    if ret:

        # burada otoparka filtre uygulayarak farkları daha net hale getiriyoruz.
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 1)
        img_Threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,16)
        img_median = cv2.medianBlur(img_Threshold, 5)
        img_Dilate = cv2.dilate(img_median, np.ones((3,3)), iterations = 1) # kalınlaştırma
        
        
        CheckParkSpace(img_Dilate)
    
        cv2.imshow('video', img)
       # cv2.imshow('vido', img_gray )
        #cv2.imshow('video', img_blur)
       # cv2.imshow('video_Th', img_Threshold)
        #cv2.imshow('video_median', img_median)
        #cv2.imshow('img_Dilate', img_Dilate)
    else:
        break
    k = cv2.waitKey(200)
    if k == 27:
        break
    
cv2.destroyAllWindows()