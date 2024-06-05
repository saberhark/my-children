import numpy as np
import cv2
from PIL import ImageGrab
import easyocr
import time

# EasyOCR 리더 객체 생성 (한국어)
try:
    reader = easyocr.Reader(['ko'])
except AttributeError:
    print("Error initializing EasyOCR Reader: Check PyTorch installation and compatibility.")

def screen_capture():
    # 전체 화면 캡처
    screen = np.array(ImageGrab.grab(bbox=None))
    # 캡처된 이미지를 회색조로 변환
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return gray_screen

def ocr_processing(image):
    # OCR을 통해 이미지에서 텍스트 추출
    results = reader.readtext(image, detail=0)  # detail=0은 텍스트만 반환
    text = ' '.join(results)  # 추출된 텍스트를 하나의 문자열로 결합
    return text

def check_text(text, target):
    # 텍스트 내에 특정 문자열이 있는지 확인
    return target in text

def main():
    target_text = "안전한 장소에서 창을 3번 클릭하세요"
    while True:
        image = screen_capture()
        extracted_text = ocr_processing(image)
        if check_text(extracted_text, target_text):
            print(f"'{target_text}' detected!")
        else:
            print(extracted_text)
        # 1분 간격으로 반복
        time.sleep(60)

if __name__ == "__main__":
    main()
