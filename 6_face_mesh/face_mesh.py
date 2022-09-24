import cv2
import mediapipe as mp

cap = cv2.VideoCapture('video3.mp4')

mpMesh = mp.solutions.face_mesh
mesh = mpMesh.FaceMesh(max_num_faces=1)
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)


while True:
    
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = mesh.process(img_rgb)
    #print(result.multi_face_landmarks)
    
    if result.multi_face_landmarks:
            
        for fmland in result.multi_face_landmarks:
            mpDraw.draw_landmarks(img, fmland, mpMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
    
    
    if success == True:
        cv2.imshow('video',img)
    
    k = cv2.waitKey(40)
    if k ==27:
        break
    
cv2.destroyAllWindows()