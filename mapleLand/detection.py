import cv2
import numpy as np
import torch
from PIL import ImageGrab, ImageDraw

# YOLOv5 모델 로드 (사전 학습된 모델 경로를 지정해야 함)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='../yolov5/runs/train/exp12/weights/best.pt', force_reload=True)

# 객체 탐지 및 처리
def detect_and_process(area):
    # 화면 캡처
    screenshot = ImageGrab.grab(bbox=area)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 이미지를 그레이스케일로 변환
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    # 객체 탐지
    results = model(gray_frame)

    # 탐지된 객체의 좌표 추출
    detections = results.pandas().xyxy[0]

    # 탐지된 객체가 있으면 스크린샷에 경계 상자 그리기
    if not detections.empty:
        print("Detected objects:")
        draw = ImageDraw.Draw(screenshot)
        for index, detection in detections.iterrows():
            class_name = detection['name']
            xmin, ymin, xmax, ymax = detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax']
            print(f"{class_name} detected at [{xmin}, {ymin}, {xmax}, {ymax}]")
            draw.rectangle([xmin, ymin, xmax, ymax], outline="red")
            draw.text((xmin, ymin), class_name, fill="yellow")
        del draw

    return screenshot

