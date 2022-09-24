import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


cap = cv2.VideoCapture('video2.mp4')

detector = FaceMeshDetector()
plotY = LivePlot(540, 360, [10, 60]) #(videosize,, plot eksen değerleri,,)
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243] # gözün çevresinin idleri
color = (0,0,255)
ratioList = []
counter = 0
blickCounter = 0

while True: 
    ret, img = cap.read()
    if ret:
        img, faces = detector.findFaceMesh(img, draw = False)
        
        if faces:
            face = faces[0]
            
            for id in idList:
                cv2.circle(img, face[id], 5, color, cv2.FILLED)
            # gözün belirli noktalarını değişkenlere aktarıyoruz
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            # dikey olarak aradaki farkı tespit edeceğiz
            lengthVer, _ = detector.findDistance(leftUp, leftDown) # dikey mesafe
            lengthHor, _ = detector.findDistance(leftLeft, leftRight)
            # göze + şekline benzer bi şekil çiziyoruz
            cv2.line(img, leftUp, leftDown, (0,255,0),3)
            cv2.line(img, leftLeft, leftRight, (0,255,0),3)
            
            ratio = int((lengthVer/lengthHor)*100)
            ratioList.append(ratio)
            # ratioList i 3 elemanlı hale getiriyoruz. böylelikle göz kırptığı an ortalama düşüyor ve sonucu alıyoruz
            if len(ratioList) >3:
                ratioList.pop(0)
                
            ratioAvg = sum(ratioList)/len(ratioList)
            # threshold ekliyoruz 
            if ratioAvg < 35 and counter == 0:
                blickCounter += 1
                counter = 1
            #print(counter)
            if counter !=0:
                counter +=1
                if counter >10:
                    counter = 0
            cvzone.putTextRect(img, f'BlinkCount:{blickCounter}', (50,100), colorR=color)
            # canlı olarak bir çizgi grafiğinde sonuçlar çıkaracağız
            imgPlot = plotY.update(ratioAvg, color)
            img = cv2.resize(img,(640,360))
            imgStack = cvzone.stackImages([img, imgPlot],2,1)
           
        
        cv2.imshow('video', imgStack)
        
        k = cv2.waitKey(15)
        if k == 27:
            break
        
    else:
        break
cap.release()
cv2.destroyAllWindows()