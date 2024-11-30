from requests.auth import HTTPBasicAuth
from io import BytesIO
from pprint import pprint

import requests
import cv2
import os
import sys
import time
import serial

ser = serial.Serial("/dev/ttyACM0", 9600)

# API endpoint
api_url = ""

URL ='http://192.168.10.13:8882/inference/run'

def get_img():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera Error")
        exit(-1)

    ret, img = cam.read()
    cam.release()

    return img
    
def crop_img(img, size_dict):
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    img = img[y : y + h, x : x + w]
    return img
    
def detect(img):
    print(img)
    a,b=0,20
    color= [0,0,255]
    thinkness=1
    name = ''
    x1,y1=0,0
    x2,y2=0,0
    font=cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.7
    class_start_point = [0,25]
    
    class_cnt = {'1':0,'2':0,
			'3':0,'4':0,
			'5':0,'6':0}
			
    class_name = {'1':"BOOTCELL",'2':"CHIPSET",
			'3':'HOLE','4':"OSILATOR",
			'5':'PICO','6':'USB'}
			
    color_lst = {'1':[0,0,255],'2':[255,0,0],
                '3':[0,255,0],'4':[255,255,0],
                '5':[0,255,255],'6':[20,100,150]}

    image = open(img, "rb").read()

    response = requests.post(
        url=URL,
        files={'file':image},
    )

    result = response.json()['objects']
    print(result)

    img = cv2.imread(img)
    
    for i in result:
        name = i['class_number']
        class_cnt[str(name)] += 1
        x1,y1,x2,y2 = i['bbox']
        start_point1=[int(x1-a),int(y1-b)]
        start_point=[int(x1),int(y1)]
        end_point=[int(x2),int(y2)]

        cv2.rectangle(img,start_point,end_point,color_lst[str(name)],thinkness)
        cv2.putText(img,str(name),start_point1,font,font_scale,color_lst[str(name)],thinkness) 

    for j in class_cnt:
        text = class_name[j] +': '+str(class_cnt[j])
        cv2.putText(img,text,class_start_point,font,font_scale,color_lst[j],thinkness)

        class_start_point[1] += 25
    return img
    
    
def main():
    folder_name = 'img_3'
    detect_folder = 'detect_img_1'
    start_num = int(input('start_num: '))

    while 1:
        data = ser.read()
        print(data)
        if data == b"0":
            img = get_img()
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            if not os.path.exists(detect_folder):
                os.makedirs(detect_folder)
			
            detect_path = os.path.join(os.getcwd(),detect_folder,str(start_num)+".jpg")
            img_path = os.path.join(os.getcwd(),folder_name,str(start_num)+".jpg")
            
            cv2.imshow("origin_img", img)
            cv2.imwrite(img_path,img)
            detect_img = detect(img_path)
	    
            cv2.imshow("detect_img", detect_img)
            cv2.imwrite(detect_path,detect_img)
            start_num +=1
            print(img_path)
            cv2.waitKey(1)
            ser.write(b"1")
        else:
            pass
		
if __name__ == '__main__':
	main()
