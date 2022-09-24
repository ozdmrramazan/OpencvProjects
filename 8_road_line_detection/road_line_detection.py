import cv2
import numpy as np


cap = cv2.VideoCapture('video1.mp4')


def drawLines(image, lines):
    image = np.copy(image)
    image_blank = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image_blank, (x1,y1), (x2,y2), (0,255,0), thickness = 10)
    
    image = cv2.addWeighted(image, 0.8, image_blank, 1, 0.0)
    return image


def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    
    match_mask_color = 255
    
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_img = cv2.bitwise_and(image,mask)
    
    return masked_img



def Process(image):
    h, w,_= image.shape
    
    region_of_interest_vertices = [(0,h), (w/2, h/2), (w, h)] 
    # (0,h) sol alt köşe, (w/2, h/2) resmin tam ortası, (w,h) resmin sağ alt köşesi. bir üçgen oluşturduk
    
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Canny(img, threshold1, threshold2)  threshold1 ve threshold2 arasındaki çizgileri alır
    img_canny = cv2.Canny(img_gray, 250, 120) # çizgi tespiti
    img_cropped = region_of_interest(img_canny, np.array([region_of_interest_vertices], np.int32))
    # croppe işleminden sonra son resimdeki çizgileri tespit edeceğiz.
    lines = cv2.HoughLinesP(img_cropped, rho = 2, theta = np.pi/180, threshold = 200, lines = np.array([]), minLineLength = 150, maxLineGap=4)
    imageWithLine = drawLines(image, lines)
    return imageWithLine
        

while True:
    ret, img = cap.read()
    if ret:
        img_process = Process(img)

        cv2.imshow('Video',img_process)
    else:
        break
    
    k = cv2.waitKey(20)
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()