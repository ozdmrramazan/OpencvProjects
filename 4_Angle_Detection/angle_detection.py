"""
Burada 3 tane nokta belirleyip aralarındaki açıya göre hareketinin sonucunu yazdıracağız.
Burada hedefimiz dizini açıp kapatma hareketinin tespiti ve kaç kez tekrarlandığının sayısını bulmak.
"""

import cv2
import mediapipe as mp
import numpy as np
import math
# nesneleri oluşturduk
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture('video2.mp4')
dir = 0
count = 0

#Burada 3 noktayı belirleyip aralarındaki açıyı buluyoruz
def findAngle(img, p1, p2, p3, lmlist, draw = True): # draw defaut değer olarak yani hep görselleştirsin ben istemezsem yapmasın
    
    x1,y1 = lmlist[p1][1:] #zxy şeklinde nokra veriyor xy kısmını alıyorum
    x2,y2 = lmlist[p2][1:]
    x3,y3 = lmlist[p3][1:]
    
    # 3 noktanın x ve y noktalarını biliyoruz. Şimdi açıyı hesaplayacağız
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    if angle < 0 : angle +=360
    # noktaları görselleştiriyoruz 
    if draw:
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 3)
        cv2.line(img, (x3,y3), (x2,y2), (0,0,255), 3)
        
        cv2.circle(img, (x1,y1), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img, (x3,y3), 10, (0,255,255), cv2.FILLED)
        
        cv2.circle(img, (x1,y1), 15, (0,255,255))
        cv2.circle(img, (x2,y2), 15, (0,255,255))
        cv2.circle(img, (x3,y3), 15, (0,255,255))
        # açıyı yerleştiriyoruz videoya
        cv2.putText(img, str(int(angle)), (x2-40, y2+40), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2)
    
    return angle
    

while True:
    
    success, img = cap.read()
    
    if success == True:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)
        if result.pose_landmarks:
            
            lmlist = []
            mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
            
            for id,lm in enumerate(result.pose_landmarks.landmark):
                h,w,_ = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)    
                lmlist.append([id,cx,cy])
                
        
        if len(lmlist) !=0:
          #şınav açıları hesaplicaz Açı için 3 nokta lazım
          
          #angle = findAngel(img, 11, 13, 15, lmlist)
          #per = np.interp(angle, (185, 245), (0, 100))
          #print(angle)
          # video2
          angle = findAngle(img, 23, 25, 27, lmlist)
          # bu açıyı 120 80 aralığından geçtiğinde anahtar gibi 0 veya 100 oluyor per.
          per = np.interp(angle, (120, 80), (0, 100))
          #print(per, angle)
          if per ==100:
              if dir == 0:
                  count += 0.5
                  dir=1
          # per bu if koşullarına değişmediği sürece 1 defa girebilir dir iler ters bağlı
          if per ==0:
              if dir == 1:
                  count += 0.5
                  dir=0
                  
          #print(count)
          cv2.putText(img, str(int(count)), (45, 125), cv2.FONT_HERSHEY_PLAIN, 10, (0,255,255), 2)  
          
        
          cv2.imshow('video', img)
    else:
        break

    k=cv2.waitKey(50)
    
    if k == 27:
        break
    
cv2.destroyAllWindows()







    