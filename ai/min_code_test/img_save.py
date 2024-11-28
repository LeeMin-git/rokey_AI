import cv2
import os
cnt=0
def main():
    global cnt
    cam = cv2.VideoCapture(0)
    folder = input('folder name: ')
    
    while cam.isOpened():
        ret,img = cam.read()
        cv2.imshow('img',img)
        input_key = cv2.waitKey(1) 
        if input_key == ord('c'):
            frame_path = os.path.join(os.getcwd()+"/"+folder, str(cnt)+".jpg")
            if not os.path.exists(folder):
                os.makedirs(folder)
            cv2.imwrite(frame_path,img)
            print(frame_path)
            cnt +=1
        elif input_key == ord('z'):
            cam.release()
            cv2.destroyAllWindows()

main()
    
