import cv2
import mediapipe as mp

cap = cv2.VideoCapture('video3.mp4')
# Nesneleri oluştruduk
mpPose= mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

while True:
    
    success, img = cap.read()
    if success == True:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)
        
        if result.pose_landmarks:            
            mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
                 
    
        
        cv2.imshow('hii',img)
    else:
        break
    k = cv2.waitKey(50)
    if k == 27:
        break

cv2.destroyAllWindows()