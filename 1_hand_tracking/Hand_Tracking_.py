"""
Fps eğer kameranızı aktif ederseniz sonuçları üretir.
kamera aktif etmek için 
cap = cv2.VideoCapture(0) yapmalısınız
"""
import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture('hand.jpg')

# el tespiti için nesneyi oluşturduk
mpHand= mp.solutions.hands
hands= mpHand.Hands()   
# Çizim için gerekli nesneyi oluşturduk
mpDraw= mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles # tasarım

# fps için değişkenler
pTime=0
cTime=0
 
while True:
    ret,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # default değer bgr rgb e çeviriyoruz
    
    result = hands.process(imgRGB) 
    #print(result.multi_hand_landmarks) 
    
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            
            ## Elimin açık mı kapalı mı olduğunu tespit etmek için koordinatları alıyoruz
            x,y= handLms.landmark[9].x, handLms.landmark[9].y
            x1,y1= handLms.landmark[12].x, handLms.landmark[12].y
             
            if y1>y:
                cv2.putText(img, 'KAPALI', (400,75), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,0), 3)
            else:
                cv2.putText(img, 'ACIK', (400,75), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 3)
            ## 
            
            
            
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS,
                                  mp_drawing_styles.get_default_hand_landmarks_style(),
                                  mp_drawing_styles.get_default_hand_connections_style())            
            
            # Belirli bir bölge işaretleme
            for id, lm in enumerate(handLms.landmark): 
                print(id,lm)
                h, w, c = img.shape
                
                """
                lm : x: 0.27233538031578064
                    y: 0.5325449705123901
                    z: -0.12955856323242188
                    
                lm.x : 0.27233538031578064
                """
                cx, cy = int(lm.x*w), int(lm.y*h)  # koordinatları aldık
                
                #bilek işaretleme
                if id==0:
                    cv2.circle(img, (cx,cy), 9, (255,0,0), cv2.FILLED)
                    
                    
    #fps
    cTime = time.time()
    fps= 1/ (cTime - pTime)
    pTime=cTime
    #  cv2.putText(resim, text , konum, font, , renk, kalınlık)
    cv2.putText(img, 'FPS: '+str(int(fps)), (10,75), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
    
    
                
    cv2.imshow('Video',img)
    k = cv2.waitKey(2) & 0XFF 
    
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()

