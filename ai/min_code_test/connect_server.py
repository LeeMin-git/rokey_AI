import requests
import os
import time
def test_image_detection():
    # API endpoint URL
    url = "http://192.168.10.13:8882/inference/run"  # Adjust port if different

    # Test image path - adjust this to your image location
    image_path = "/home/spb/workspace/kdt-solutions-main/server/pico.jpg"
    
    # Parameters
    params = {
        "min_confidence": 0.6,
        "base_model": "YOLOv6-N" # YOLOv6-N, YOLOv6-M, YOLOv6-L, YOLOv6-L6
    }
    
    # Prepare the file
    with open(image_path, 'rb') as image_file:
        files = {'file': ('image.jpg', image_file, 'image/jpeg')}
        
        # Send POST request
        response = requests.post(url, params=params, files=files)
    
    # Check if request was successful
    if response.status_code == 200:
        print("Success!")
        print("Detected objects:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_start_server():
    # API endpoint URL
    url = "http://192.168.10.13:8888/start-server/team2"  # Adjust host/port and team name
    # Parameters
    params = {
        "model_id": "6b204981-efe3-4d72-a112-e8e5019cb9fd"  # Replace with actual model ID
    }
    
    # Send POST request
    response = requests.post(url, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        print("Server started successfully!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Test both endpoints
    print("Testing server start...")
    test_start_server()
    
    time.sleep(1)
    
    print("\nTesting image detection...")
    test_image_detection()