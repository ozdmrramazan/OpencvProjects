import cv2
import pickle

# mouse ile tıklayarak seçtiğimiz alana bir kare atıp dolumu boş mu işaretliyoruz
try:
    with open('CarParkPos','rb') as p:
        posList = pickle.load(p)
except:        
    posList = []

width = 20
height = 9

def mouseClick(events, x, y, flags, params):
    # kare alan oluşturma
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    # kare alan silme
    if events == cv2.EVENT_RBUTTONDOWN:
        for id, pos in enumerate(posList):
            x1,y1 = pos
            # tıkladığım alan karenin içindeyse sil  şöyle karenin sol alt köşesi 0,0 noktası gibi düşün
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(id)
    with open('CarParkPos','wb') as p:
        pickle.dump(posList, p)


while True:
    img = cv2.imread('first_frame.png')
    
    for pos in posList:
        
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0,255,255), 2)
    
    cv2.imshow('img',img)
    print(posList)
    cv2.setMouseCallback('img', mouseClick)    
    
    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()