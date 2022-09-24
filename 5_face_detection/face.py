import cv2
import mediapipe as mp

# Nesneleri Oluşturuyoruz
mpFace= mp.solutions.face_detection
face= mpFace.FaceDetection(min_detection_confidence = 0.01)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture('video3.mp4')

while True:
    ret, img = cap.read()
    if ret == True:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = face.process(img_rgb)
        
        #print(result.detections)
        
        if result.detections:
            for id,detection in enumerate(result.detections):
                """
                location_data.relative_bounding_box bize 4 değer dönürüyor
                xmi0n ymin width height. 
                bu değerleri bi kutu çizmek için kullanacağız
                """
                bboxC = detection.location_data.relative_bounding_box
                #print(bboxC)
                h, w,_ = img.shape
                
                bbox= int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w), int(bboxC.height*h)
                #print(bbox)
                cv2.rectangle(img,bbox,(0,255,255),2)
        
    
        cv2.imshow('video',img)
    else:
        break
    k = cv2.waitKey(1)
    if k ==27:
        break
    
cv2.destroyAllWindows()