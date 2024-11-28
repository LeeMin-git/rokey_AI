import requests
from requests.auth import HTTPBasicAuth
import cv2
import os

# URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/12f80a0d-9fe2-44bd-948a-5f191671c333/inference"
URL ='https://suite-endpoint-api-apne2.superb-ai.com/endpoints/456a68c5-b226-4292-9380-05155fbcdd47/inference'
ACCESS_KEY = "WpML0KMYxjSAzChtIdDNaXWQTpPQwmW7utBS02L2"
TEAM_NAME = 'kdt2024_1-12'

class_cnt = {'RASPBERRY PICO':0,'CHIPSET':0,
                'USB':0,'HOLE':0,
                'OSCILLATOR':0,'BOOTCEL':0}

data_set = os.listdir('./ai/min_code_test/normal') #여기 

for data in data_set:
    img_set = data
    IMAGE_FILE_PATH = "./ai/min_code_test/normal/"+img_set # 이미지 하나 #여기

    image = open(IMAGE_FILE_PATH, "rb").read()

    response = requests.post(
        url=URL,
        auth=HTTPBasicAuth(TEAM_NAME, ACCESS_KEY),
        headers={"Content-Type": "image/jpeg"},
        data=image,
    )

    result = response.json()['objects']
    print(result)

    img_path = './ai/min_code_test/normal/'+img_set #여기
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
    color_lst = {'RASPBERRY PICO':[0,0,255],'CHIPSET':[255,0,0],
                'USB':[0,255,0],'HOLE':[255,255,0],
                'OSCILLATOR':[0,255,255],'BOOTCEL':[20,100,150]}

    for i in result:
        name = i['class']
        class_cnt[name] += 1
        x1,y1,x2,y2 = i['box']
        start_point1=[x1-a,y1-b]
        start_point=[x1,y1]
        end_point=[x2,y2]

        cv2.rectangle(img,start_point,end_point,color_lst[name],thinkness)
        cv2.putText(img,name,start_point1,font,font_scale,color_lst[name],thinkness) 

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

#퍼센트를 나타내기 위해서 생성
cv2.destroyAllWindows()