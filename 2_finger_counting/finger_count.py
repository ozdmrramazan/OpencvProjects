"""
Burada parmak sayma işlemi yaparken önemli bir noktadan bahsedeceğim.
Baş parmak için bi alt eklem noktasının x eksenine göre değişimine göre sonuçlandırdık ve
Sağ ve Sol el için ayrı ayrı işlemler yaptık

"""


import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

# neseneleri oluşturduk
mpholistic= mp.solutions.holistic
holistic=mpholistic.Holistic()
mpdraw=mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

tipIDs =  [4, 8, 12, 16, 20]

# Çizimi gerçekleştirirken her bir eklemin id numarasını ve koordinatlarını bir listeye atıyoruz 
def handslms(result):
    mpdraw.draw_landmarks(img, result, mpholistic.HAND_CONNECTIONS,
                              mp_drawing_styles.get_default_hand_landmarks_style(),
                              mp_drawing_styles.get_default_hand_connections_style())

    for id,lm in enumerate(result.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x*w), int(lm.y*h)
        lmlist.append([id,cx,cy])


while True:
    success, img = cap.read()
    rgb_img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    result = holistic.process(rgb_img)
    #print(result.multi_hand_landmarks)
    
    lmlist=[]
    # ekrandaki konumuna göre sağ mı sol mu tespiti yapılıp ona göre işlemler yapılıyor.
    if result.right_hand_landmarks:
        handslms(result.right_hand_landmarks)
    if result.left_hand_landmarks:
        handslms(result.left_hand_landmarks)
        # işaretleme ekstra olarak
            # işaret uç 8
            #if id == 8:
            #    cv2.circle(img, (cx,cy), 9, (255,0,0), cv2.FILLED)
            # işaret uç 6
            #if id == 6:
            #    cv2.circle(img, (cx,cy), 9, (0,0,255), cv2.FILLED)
    
    if len(lmlist) !=0:
        fingers = []
        
        # bas parmak
        # sağ el
        if result.right_hand_landmarks:
            if lmlist[tipIDs[0]][1]> lmlist[tipIDs[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        # sol el
        if result.left_hand_landmarks:
             if lmlist[tipIDs[0]][1]< lmlist[tipIDs[0]-1][1]:
                fingers.append(1)
             else:
                fingers.append(0)
        # baş parmak dışındaki parmakların konumuna göre sonuçları listeye atardık.
        for id in range(1,5):
            if lmlist[tipIDs[id]][2] < lmlist[tipIDs[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        totalF= fingers.count(1)

        cv2.putText(img, str(totalF), (30,125), cv2.FONT_HERSHEY_PLAIN, 10,(255,0,0),8)
        
    
    cv2.imshow('img',img)
    
    k= cv2.waitKey(1)  
    
    if k==27:
        break
    
cv2.destroyAllWindows()
