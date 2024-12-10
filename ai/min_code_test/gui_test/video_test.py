import cv2
cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret,img=cam.read()
    cv2.imshow('test',img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        cam.release()
        cv2.destroyAllWindows()
        