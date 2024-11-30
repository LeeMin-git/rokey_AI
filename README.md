<2024-11-29 금>
- 기존에 제공한 이미지 모두 지우고 다시 라벨링
- 데이터 셋을 늘리니 인식도가 높아짐
- 코드를 통해 superb AI 플렛폼에 생성한 모델을 서버에 올려서 사용함 (connect_server, total 코드 참조)
- 컨베이어 벨트에서 센서로 인식한 물체의 사진을 저장하고 해당 사진을 서버로 보내 object detect 한 다음 OpenCV를 통해 창을 띄우는 코드 생성(total)
- 인식한 이미지를 db에 쓰는 코드 및 생성하는 코드와 연동 해야함.

<2024-11-28 목>
- 라벨링 다시함.
- img_save.py는 웹캠을 통해 c를 누르면 사진 저장하고 d를 누르면 종료함
- 데이터 30개 정도 추가함.

<2024-11-27 수>
- superb AI(https://platform.superb-ai.com)플랫폼을 통해 생성한 모델을 통해 이미지 인식률 확인
- url을 통해 테스트하는 방법을 python으로 구현
- 인식 후 날라오는 데이터와 OpenCV를 활용하여 바운딩 박스 및 인식 개수 확인
- yolov8을 활용하여 object 탐지
- Steamlit(https://streamlit.io)과 그라디오(https://www.gradio.app/)를 활용하여 웹에서 확인 하는 코드 생성
