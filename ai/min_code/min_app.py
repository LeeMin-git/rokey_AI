import cv2
import gradio as gr
import requests
import numpy as np
from PIL import Image
from requests.auth import HTTPBasicAuth


# 가상의 비전 AI API URL (예: 객체 탐지 API)
VISION_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/12f80a0d-9fe2-44bd-948a-5f191671c333/inference"
ACCESS_KEY = "WpML0KMYxjSAzChtIdDNaXWQTpPQwmW7utBS02L2"
TEAM = 'kdt2024_1-12'
a,b=0,20
color= [0,0,255]
thinkness=1
name = ''
x1,y1=0,0
x2,y2=0,0
font=cv2.FONT_HERSHEY_COMPLEX
font_scale = 1
class_start_point = [0,25]




def process_image(image):
    # 이미지를 OpenCV 형식으로 변환
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 이미지를 API에 전송할 수 있는 형식으로 변환
    _, img_encoded = cv2.imencode(".jpg", image)
    
    byte_image = bytes(img_encoded)


    response = requests.post(
        url=VISION_API_URL,
        auth=HTTPBasicAuth(TEAM, ACCESS_KEY),
        headers={"Content-Type": "image/jpeg"},
        data=byte_image,
    )

    result = response.json()['objects']
    print(result)

    class_cnt = {'RASPBERRY PICO':0,'CHIPSET':0,
                'USB':0,'HOLE':0,
                'OSCILLATOR':0,'BOOTCEL':0}

    color_lst = {'RASPBERRY PICO':[0,0,255],'CHIPSET':[255,0,0],
                'USB':[0,255,0],'HOLE':[255,255,0],
                'OSCILLATOR':[0,255,255],'BOOTCEL':[255,255,255]}

    for i in result:
        name = i['class']
        class_cnt[name] += 1
        x1,y1,x2,y2 = i['box']
        start_point1=[x1-a,y1-b]
        start_point=[x1,y1]
        end_point=[x2,y2]

        cv2.rectangle(image,start_point,end_point,color_lst[name],thinkness)
        cv2.putText(image,name,start_point1,font,font_scale,color_lst[name],thinkness) 

    color= [0,0,255]
    for j in class_cnt:
        text = j +': '+str(class_cnt[j])
        cv2.putText(image,text,class_start_point,font,font_scale,color_lst[j],thinkness)

        
        
        class_start_point[1] += 25


    # API 호출 및 결과 받기 - 실습1

    # API 결과를 바탕으로 박스 그리기 - 실습2

    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image)


# Gradio 인터페이스 설정
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil"),
    outputs="image",
    title="Vision AI Object Detection",
    description="Upload an image to detect objects using Vision AI.",
)

# 인터페이스 실행
iface.launch(share=True) ## (share=True)하면 나타나는 url을 통해 외부에서도 사용이 가능함
