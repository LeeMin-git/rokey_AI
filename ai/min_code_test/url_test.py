import requests
from requests.auth import HTTPBasicAuth

URL ='https://suite-endpoint-api-apne2.superb-ai.com/endpoints/456a68c5-b226-4292-9380-05155fbcdd47/inference'
TEAM_NAME = 'kdt2024_1-12'


IMAGE_FILE_PATH = "0.jpg" # 이미지 하나 #여기

image = open(IMAGE_FILE_PATH, "rb").read()

response = requests.post(
    url=URL,
    data=image
)

result = response.json()['objects']
print(result)