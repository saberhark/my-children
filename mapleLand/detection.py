'''
exp16 >> 0.3커버 only 적용 200 epoch >> 동전이 많이 떨어지면 잡지 못함
exp >> 0.3, 0.5 동시 적용 200 epoch >> 생성 중
exp2 >> 0.3, 0.5 동시 적용 100 epoch >> 생성 중
exp3 >> 0.3, 0.5 / crop 추가 적용 100 epoch
exp4 >> 0.3, 0.5 동시 적용 200 epoch
exp4 >> 0.3, 0.5 동시 적용 200 epoch

'''

import cv2
import numpy as np
import torch
from PIL import ImageGrab, ImageDraw
import pyautogui
import time

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='../yolov5/runs/train/exp5/weights/best.pt', force_reload=False)

# 객체 탐지 및 처리 함수
def detect_and_process(area, character_position, prev_position):
    position = None
    # 화면 캡처
    screenshot = ImageGrab.grab(bbox=area)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 이미지를 그레이스케일로 변환
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    # 객체 탐지
    results = model(gray_frame)
    detections = results.pandas().xyxy[0]

    # 케릭터의 상대적 좌표 변환
    character_x, character_y = character_position
    area_x1, area_y1, area_x2, area_y2 = area
    relative_character_x = character_x - area_x1
    relative_character_y = character_y - area_y1


    # 케릭터와 몬스터의 거리 범위
    max_horizon = 300
    max_vertical = 100 # 같은 라인, 100 정도 까지는 커버됨

    closest_distance = float('inf')
    valid_object_detected = None

    # 탐지된 객체가 있으면 처리
    if not detections.empty:
        print("Detected objects:")
        draw = ImageDraw.Draw(screenshot)
        for index, detection in detections.iterrows():
            xmin, ymin, xmax, ymax = detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax']
            object_height = ymax - ymin

            # 객체 높이가 50보다 큰 경우만 처리
            if object_height > 60:
                if abs(xmin-relative_character_x)<80:
                    continue
                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2

                # 객체와 케릭터 사이의 거리 계산
                distance = np.sqrt((x_center - relative_character_x) ** 2 + (y_center - relative_character_y) ** 2)

                # 가장 가까운 객체 찾기
                if distance < closest_distance:
                    closest_distance = distance
                    position = "left" if x_center < relative_character_x else "right"

                # 캔버스에 경계 상자 그리기
                draw.rectangle([xmin, ymin, xmax, ymax], outline="red")
                draw.text((xmin, ymin), detection['name'], fill="yellow")

                # 몬스터가 케릭터와의 유효 범위 이내에 있는 경우에만 유효한 객체로 처리
                if abs(relative_character_x - x_center) < max_horizon and abs(relative_character_y - y_center) < max_vertical:
                    valid_object_detected = detection
                else:
                    print("범위 밖")


        del draw

    # 유효한 객체가 탐지된 경우에만 키보드 동작 수행
    if valid_object_detected is not None and position is not None:
        class_name, xmin, ymin, xmax, ymax = detection['name'], detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax']

        if position == "left" and position != prev_position:
            pyautogui.press('left')
            time.sleep(0.1)
        elif position == "right" and position != prev_position:
            pyautogui.press('right')
            time.sleep(0.1)
        pyautogui.press('f')
        time.sleep(1.0)
        print(f"{class_name} detected at [{xmin}, {ymin}, {xmax}, {ymax}], Position: {position}, Character: ({relative_character_x}, {relative_character_y}), center_x_y: {(xmin+xmax)/2}, {(ymin+ymax)/2}")


    return screenshot, position
