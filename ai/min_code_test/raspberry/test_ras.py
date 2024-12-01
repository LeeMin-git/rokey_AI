import requests
from requests.auth import HTTPBasicAuth
import cv2
import os
import sys

# URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/12f80a0d-9fe2-44bd-948a-5f191671c333/inference"
URL ='http://192.168.10.13:8882/inference/run'
img_path = './img/new_data4'



data_set = os.listdir('./img/new_data4') 

for data in data_set:
    img_set = data
    IMAGE_FILE_PATH = os.path.join('./img/new_data4',img_set)
    class_cnt = {'1':0,'2':0,
                '3':0,'4':0,
                '5':0,'6':0}

    image = open(IMAGE_FILE_PATH, "rb").read()

    response = requests.post(
        url=URL,
        files={'file':image},
    )

    result = response.json()['objects']
    print(result)

    img_path = os.path.join('./img/new_data4',img_set) #여기
    img = cv2.imread(img_path)

    a,b=0,20
    color= [0,0,255]
    thinkness=1
    name = ''
    x1,y1=0,0
    x2,y2=0,0
    font=cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    class_start_point = [0,25]
    color_lst = {'1':[0,0,255],'2':[255,0,0],
                '3':[0,255,0],'4':[255,255,0],
                '5':[0,255,255],'6':[20,100,150]}

    for i in result:
        name = i['class_number']
        class_cnt[str(name)] += 1
        x1,y1,x2,y2 = i['bbox']
        start_point1=[int(x1-a),int(y1-b)]
        start_point=[int(x1),int(y1)]
        end_point=[int(x2),int(y2)]

        cv2.rectangle(img,start_point,end_point,color_lst[str(name)],thinkness)
        cv2.putText(img,str(name),start_point1,font,font_scale,color_lst[str(name)],thinkness) 

    color= [0,0,255]
    for j in class_cnt:
        text = j +': '+str(class_cnt[j])
        cv2.putText(img,text,class_start_point,font,font_scale,color_lst[j],thinkness)

        
        
        class_start_point[1] += 25


    cv2.imshow(data,img)
    if cv2.waitKey(0) == ord('c'):
        continue
    elif cv2.waitKey(0) == ord('d'):
        cv2.destroyWindow(data)
        
    elif cv2.waitKey(0) == ord('z'):
        cv2.destroyAllWindows()
        sys.exit()

#퍼센트를 나타내기 위해서 생성
cv2.destroyAllWindows()
