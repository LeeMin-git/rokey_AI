# import requests
# from requests.auth import HTTPBasicAuth
# import os
# import cv2
# import random
# import sqlite3
# import uuid
# import io

# # URL and access key
# #URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/456a68c5-b226-4292-9380-05155fbcdd47/inference"
# URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/74da8acc-5956-4231-91d6-921f653802b5/inference"
# ACCESS_KEY = "WpML0KMYxjSAzChtIdDNaXWQTpPQwmW7utBS02L2"
# resource_folder = "/home/g1/vision-ai-inference-practice/resource/image/train_set 2024-11-27 104049"

# # Color mapping for classes
# color_dict = {
#     'RASPBERRY PICO': (0, 0, 255),
#     'USB': (0, 255, 0),
#     'BOOTCEL': (255, 0, 0),
#     'CHIPSET': (255, 255, 0),
#     'OSCILLATOR': (255, 0, 255),
#     'HOLE': (0, 255, 255)
# }

# # Initialize counters
# total_cnt = 106
# total_hole_cnt = 106 * 4
# correct = 0

# class_correct = {
#     'RASPBERRY PICO': 0,
#     'USB': 0,
#     'BOOTCEL': 0,
#     'CHIPSET': 0,
#     'OSCILLATOR': 0,
#     'HOLE': 0
# }

# class_total = {
#     'RASPBERRY PICO': 0,
#     'USB': 0,
#     'BOOTCEL': 0,
#     'CHIPSET': 0,
#     'OSCILLATOR': 0,
#     'HOLE': 0
# }

# # Prepare the list of jpg files for processing
# jpg_files = [os.path.join(resource_folder, file) for file in os.listdir(resource_folder) if file.endswith(".jpg")]


# # Process each image file
# for jpg_file in jpg_files:
#     print(f"Processing file: {jpg_file}")
#     with open(jpg_file, "rb") as img_file:
#         image = img_file.read()

#     # Send image to inference service
#     response = requests.post(
#         url=URL,
#         auth=HTTPBasicAuth("kdt2024_1-12", ACCESS_KEY),
#         headers={"Content-Type": "image/jpeg"},
#         data=image,
#     )

#     if response.status_code != 200:
#         print(f"Error with file {jpg_file}: {response.status_code}")
#         continue

#     # Get the response in JSON format
#     obj_dict = response.json()
#     img = cv2.imread(jpg_file)
#     class_text_start_point = [0, 20]
#     obj_name_count = {}

#     # Count the objects detected
#     for obj in obj_dict.get('objects', []):
#         class_name = obj.get('class')
#         if class_name:
#             obj_name_count[class_name] = obj_name_count.get(class_name, 0) + 1

#     # Initialize counts for each part
#     RASPBERRYPICO = USB = BOOTCEL = CHIPSET = OSCILLATOR = HOLE = 0

#     # Display the counts for each class and store in the total
#     for name, value in obj_name_count.items():
#         count_text = f"{name} : {value}"
#         if name == 'RASPBERRY PICO':
#             RASPBERRYPICO += value
#         elif name == 'USB':
#             USB += value
#         elif name == 'BOOTCEL':
#             BOOTCEL += value
#         elif name == 'CHIPSET':
#             CHIPSET += value
#         elif name == 'OSCILLATOR':
#             OSCILLATOR += value
#         elif name == 'HOLE':
#             HOLE += value

#         font = cv2.FONT_HERSHEY_SIMPLEX
#         font_scale = 0.5
#         color = color_dict.get(name, (255, 255, 255))
#         font_thickness = 1
#         cv2.putText(img, count_text, tuple(class_text_start_point), font, font_scale, color, font_thickness, cv2.LINE_AA)
#         class_text_start_point[1] += 20

#     # Determine defect status and reason
#     defect_reason = ""
#     if RASPBERRYPICO > 1:
#         is_defective = 1
#         defect_reason = "RASPBERRY PICO 부품 수 초과"
#     elif USB > 1:
#         is_defective = 1
#         defect_reason = "USB 부품 수 초과"
#     elif BOOTCEL > 1:
#         is_defective = 1
#         defect_reason = "BOOTCEL 부품 수 초과"
#     elif CHIPSET > 1:
#         is_defective = 1
#         defect_reason = "CHIPSET 부품 수 초과"
#     elif OSCILLATOR > 1:
#         is_defective = 1
#         defect_reason = "OSCILLATOR 부품 수 초과"
#     elif HOLE >= 3:
#         is_defective = 1
#         defect_reason = "HOLE 결함 (3개 이상)"
#     else:
#         is_defective = 0
#         defect_reason = "양품"

#     # Update correct counts for defect
#     if RASPBERRYPICO == 1:
#         class_correct['RASPBERRY PICO'] += 1
#     if USB == 1:
#         class_correct['USB'] += 1
#     if BOOTCEL == 1:
#         class_correct['BOOTCEL'] += 1
#     if CHIPSET == 1:
#         class_correct['CHIPSET'] += 1
#     if OSCILLATOR == 1:
#         class_correct['OSCILLATOR'] += 1
#     if HOLE == 4:
#         class_correct['HOLE'] += 1

#     # Update total counts for each class
#     class_total['RASPBERRY PICO'] += RASPBERRYPICO
#     class_total['USB'] += USB
#     class_total['BOOTCEL'] += BOOTCEL
#     class_total['CHIPSET'] += CHIPSET
#     class_total['OSCILLATOR'] += OSCILLATOR
#     class_total['HOLE'] += HOLE

#     # Draw bounding boxes and class names on the image
#     for obj in obj_dict.get('objects', []):
#         box = obj.get('box')
#         name = obj.get('class')
#         if name and box:
#             start_point = (box[0], box[1])
#             end_point = (box[2], box[3])
#             font_start_point = (box[0], box[1] - 5)
#             color = color_dict.get(name, (255, 255, 255))
#             cv2.rectangle(img, start_point, end_point, color, 2)
#             cv2.putText(img, name, font_start_point, font, 0.5, color, 1, cv2.LINE_AA)

#     # Convert image to binary
#     _, img_buffer = cv2.imencode('.jpg', img)
#     img_binary = img_buffer.tobytes()
#     # Save result to database (SQLite)
#     conn = sqlite3.connect('example.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO 제품 (datetime, uuid, is_defective, defect_reason, image)
#         VALUES (datetime('now'), ?, ?, ?, ?)
#     ''', (str(uuid.uuid4()), is_defective, defect_reason, img_binary))
#     conn.commit()
#     conn.close()

# # Calculate accuracy for each class and total accuracy
# for class_name in class_correct:
#     if class_total[class_name] > 0:
#         class_accuracy = class_correct[class_name] / class_total[class_name] * 100
#         print(f"{class_name} Accuracy: {class_accuracy:.2f}%")

# total_accuracy = correct / total_cnt * 100
# print(f"Total Accuracy: {total_accuracy:.2f}%")


import requests
from requests.auth import HTTPBasicAuth
import os
import cv2
import uuid
import sqlite3

# URL and access key
URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/74da8acc-5956-4231-91d6-921f653802b5/inference"
ACCESS_KEY = "WpML0KMYxjSAzChtIdDNaXWQTpPQwmW7utBS02L2"
resource_folder = "/home/g1/vision-ai-inference-practice/resource/image/train_set 2024-11-27 104049"

# Color mapping for classes
color_dict = {
    'RASPBERRY PICO': (0, 0, 255),
    'USB': (0, 255, 0),
    'BOOTCEL': (255, 0, 0),
    'CHIPSET': (255, 255, 0),
    'OSCILLATOR': (255, 0, 255),
    'HOLE': (0, 255, 255)
}

# Initialize counters
class_correct = {
    'RASPBERRY PICO': 0,
    'USB': 0,
    'BOOTCEL': 0,
    'CHIPSET': 0,
    'OSCILLATOR': 0,
    'HOLE': 0
}

class_total = {
    'RASPBERRY PICO': 0,
    'USB': 0,
    'BOOTCEL': 0,
    'CHIPSET': 0,
    'OSCILLATOR': 0,
    'HOLE': 0
}

# Prepare the list of jpg files for processing
jpg_files = [os.path.join(resource_folder, file) for file in os.listdir(resource_folder) if file.endswith(".jpg")]


def count_objects(obj_dict):
    """Count detected objects in the image and return counts."""
    obj_name_count = {}
    for obj in obj_dict.get('objects', []):
        class_name = obj.get('class')
        if class_name:
            obj_name_count[class_name] = obj_name_count.get(class_name, 0) + 1
    return obj_name_count


def update_class_counts(obj_name_count, class_correct, class_total):
    """Update the class counts for correct detection and total occurrences."""
    for name, value in obj_name_count.items():
        # If the class is not in the predefined dictionary, initialize it
        if name not in class_correct:
            class_correct[name] = 0
            class_total[name] = 0
        class_total[name] += value
        if value == 1:
            class_correct[name] += 1
    return class_correct, class_total


def determine_defect_status(obj_name_count):
    """Determine defect status and reason based on object counts."""
    RASPBERRYPICO = obj_name_count.get('RASPBERRY PICO', 0)
    USB = obj_name_count.get('USB', 0)
    BOOTCEL = obj_name_count.get('BOOTCEL', 0)
    CHIPSET = obj_name_count.get('CHIPSET', 0)
    OSCILLATOR = obj_name_count.get('OSCILLATOR', 0)
    HOLE = obj_name_count.get('HOLE', 0)

    defect_reason = ""
    if RASPBERRYPICO > 1:
        is_defective = 1
        defect_reason = "RASPBERRY PICO 부품 수 초과"
    elif USB > 1:
        is_defective = 1
        defect_reason = "USB 부품 수 초과"
    elif BOOTCEL > 1:
        is_defective = 1
        defect_reason = "BOOTCEL 부품 수 초과"
    elif CHIPSET > 1:
        is_defective = 1
        defect_reason = "CHIPSET 부품 수 초과"
    elif OSCILLATOR > 1:
        is_defective = 1
        defect_reason = "OSCILLATOR 부품 수 초과"
    elif HOLE >= 3:
        is_defective = 1
        defect_reason = "HOLE 결함 (3개 이상)"
    else:
        is_defective = 0
        defect_reason = "양품"
    
    return is_defective, defect_reason


def draw_boxes_and_text(img, obj_dict):
    """Draw bounding boxes and class names on the image."""
    for obj in obj_dict.get('objects', []):
        box = obj.get('box')
        name = obj.get('class')
        if name and box:
            start_point = (box[0], box[1])
            end_point = (box[2], box[3])
            font_start_point = (box[0], box[1] - 5)
            color = color_dict.get(name, (255, 255, 255))
            cv2.rectangle(img, start_point, end_point, color, 2)
            cv2.putText(img, name, font_start_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    return img


def save_to_database(is_defective, defect_reason, img_binary):
    """Save the defect information and image to SQLite database."""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO 제품 (datetime, uuid, is_defective, defect_reason, image)
        VALUES (datetime('now'), ?, ?, ?, ?)
    ''', (str(uuid.uuid4()), is_defective, defect_reason, img_binary))
    conn.commit()
    conn.close()


def process_image(jpg_file):
    """Process an image and return the response and image."""
    print(f"Processing file: {jpg_file}")
    with open(jpg_file, "rb") as img_file:
        image = img_file.read()

    # Send image to inference service
    response = requests.post(
        url=URL,
        auth=HTTPBasicAuth("kdt2024_1-12", ACCESS_KEY),
        headers={"Content-Type": "image/jpeg"},
        data=image,
    )

    if response.status_code != 200:
        print(f"Error with file {jpg_file}: {response.status_code}")
        return None, None

    # Get the response in JSON format
    obj_dict = response.json()
    img = cv2.imread(jpg_file)
    
    return obj_dict, img


def process_all_images():
    """Process all images in the resource folder and calculate accuracy."""
    global class_correct, class_total
    # Process each image
    for jpg_file in jpg_files:
        obj_dict, img = process_image(jpg_file)
        if obj_dict is None:
            continue

        obj_name_count = count_objects(obj_dict)
        is_defective, defect_reason = determine_defect_status(obj_name_count)
        
        # Draw bounding boxes and text on image
        img = draw_boxes_and_text(img, obj_dict)
        
        # Convert image to binary
        _, img_buffer = cv2.imencode('.jpg', img)
        img_binary = img_buffer.tobytes()

        # Save result to database
        save_to_database(is_defective, defect_reason, img_binary)

        # Update the class counts, including dynamically adding new classes if needed
        class_correct, class_total = update_class_counts(obj_name_count, class_correct, class_total)

    # Calculate accuracy for each class
    for class_name in class_correct:
        if class_total[class_name] > 0:
            class_accuracy = class_correct[class_name] / class_total[class_name] * 100
            print(f"{class_name} Accuracy: {class_accuracy:.2f}%")
    
    # Calculate total accuracy (assuming total count is the sum of class totals)
    total_cnt = sum(class_total.values())
    total_correct = sum(class_correct.values())
    total_accuracy = total_correct / total_cnt * 100 if total_cnt > 0 else 0
    print(f"Total Accuracy: {total_accuracy:.2f}%")


# Run the function to process all images
process_all_images()
