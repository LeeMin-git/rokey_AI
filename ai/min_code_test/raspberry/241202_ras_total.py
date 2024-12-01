#-*- coding:utf-8-*-
from requests.auth import HTTPBasicAuth
from io import BytesIO
from pprint import pprint

import requests
import cv2
import os
import sys
import time
import serial
import sqlite3
import uuid

ser = serial.Serial("/dev/ttyACM0", 9600)
start_num = 0

# API endpoint
api_url = ""

URL ='http://192.168.10.13:8882/inference/run' # 서버의 주소

total_class_cnt = {'1':0,'2':0,
			    '3':0,'4':0,
			    '5':0,'6':0} # 전체 인식된 클래스의 개수

def get_img():
    ## 카메라 구동 함수
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera Error")
        exit(-1)

    ret, img = cam.read()
    cam.release()

    return img
    
def crop_img(img, size_dict):
    ## ROI
    x = size_dict["x"]
    y = size_dict["y"]
    w = size_dict["width"]
    h = size_dict["height"]
    img = img[y : y + h, x : x + w]
    return img

def determine_defect_status(obj_name_count): 
    ## 개수를 통해 양품인지 아닌지 판단하는 코드
    """Determine defect status and reason based on object counts."""
    BOOTCEL = obj_name_count.get('1', 0)
    CHIPSET = obj_name_count.get('2', 0)
    HOLE = obj_name_count.get('3', 0)
    OSCILLATOR = obj_name_count.get('4', 0)
    RASPBERRYPICO = obj_name_count.get('5', 0)
    USB = obj_name_count.get('6', 0)

    print(RASPBERRYPICO)

    defect_reason = ""
    if not RASPBERRYPICO == 1:
        is_defective = 1
        defect_reason += "\nRASPBERRY PICO 부품 수 초과"
    if not USB == 1:
        is_defective = 1
        defect_reason += "\nUSB 부품 수 초과"
    if not BOOTCEL == 1:
        is_defective = 1
        defect_reason += "\nBOOTCEL 부품 수 초과"
    if not CHIPSET == 1:
        is_defective = 1
        defect_reason += "\nCHIPSET 부품 수 초과"
    if not OSCILLATOR == 4:
        is_defective = 1
        defect_reason += "\nOSCILLATOR 부품 수 초과"
    if HOLE > 4 or HOLE <= 3:
        is_defective = 1
        defect_reason += "\nHOLE 결함"

    if defect_reason == "":
        is_defective = 0
        defect_reason = "양품"
    
    return is_defective, defect_reason

def send_DB(is_defective,defect_reason,img_binary):
    ## 데이터 베이스로 정보를 보내는 함수
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    aa=cursor.execute('''
        INSERT INTO 제품 (datetime, uuid, is_defective, defect_reason, image)
        VALUES (datetime('now'), ?, ?, ?, ?)
    ''', (str(uuid.uuid4()), is_defective, defect_reason, img_binary))
    conn.commit()
    conn.close()

def img_detecting(img):
    ## 서버를 통해 인식한 이미지와 인식 전 이미지를 보여주는 함수
    global total_class_cnt
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
			    '5':0,'6':0} # 전체 인식된 클래스의 개수
			
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
    #print(result)

    img = cv2.imread(img)
    
    for i in result:
        name = i['class_number']
        class_cnt[str(name)] += 1
        total_class_cnt[str(name)] += 1 # 전체 개수 파악에 필요
        x1,y1,x2,y2 = i['bbox']
        start_point1=[int(x1-a),int(y1-b)]
        start_point=[int(x1),int(y1)]
        end_point=[int(x2),int(y2)]

        cv2.rectangle(img,start_point,end_point,color_lst[str(name)],thinkness)
        #cv2.putText(img,str(name),start_point1,font,font_scale,color_lst[str(name)],thinkness) 

    for j in class_cnt:
        text = class_name[j] +': '+str(class_cnt[j])
        cv2.putText(img,text,class_start_point,font,font_scale,color_lst[j],thinkness)

        class_start_point[1] += 25

    ## 코드 수정한 것이 동작을 잘하면 실행해보기
    # # Calculate accuracy for each class
    # for class_name in class_cnt:
    #     if total_class_cnt[class_name] > 0:
    #         class_accuracy = class_cnt[class_name] / total_class_cnt[class_name] * 100
    #         print(f"{class_name} Accuracy: {class_accuracy:.2f}%")

    # # Calculate total accuracy (assuming total count is the sum of class totals)
    # total_cnt = sum(total_class_cnt.values())
    # total_correct = sum(class_cnt.values())
    # total_accuracy = total_correct / total_cnt * 100 if total_cnt > 0 else 0
    # print(f"Total Accuracy: {total_accuracy:.2f}%")

    return class_cnt,img
    
def save_img():
    ## 물체를 인식한 이미지와 인식 전 이미지를 폴더에 저장하는 함수
    global start_num
    folder_name = 'img_3'
    detect_folder = 'detect_img_1'
    img = get_img()
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(detect_folder):
        os.makedirs(detect_folder)
    
    detect_path = os.path.join(os.getcwd(),detect_folder,str(start_num)+".jpg")
    img_path = os.path.join(os.getcwd(),folder_name,str(start_num)+".jpg")
    
    cv2.imshow("origin_img", img)
    cv2.imwrite(img_path,img)
    class_cnt,detect_img = img_detecting(img_path)

    cv2.imshow("detect_img", detect_img)
    cv2.imwrite(detect_path,detect_img)
    start_num +=1
    print(img_path)
    cv2.waitKey(1)
    return class_cnt,detect_img
    
def main():
    global start_num
    start_num = int(input('start_num: '))
    while 1:
        data = ser.read()
        print(data)
        if data == b"0":
            class_cnt,detect_img=save_img()
            _, img_buffer = cv2.imencode('.jpg', detect_img)
            img_binary = img_buffer.tobytes()
            is_defective,defect_reason = determine_defect_status(class_cnt)
            send_DB(is_defective,defect_reason,img_binary)

            ser.write(b"1")
        else:
            pass
		
if __name__ == '__main__':
	main()
