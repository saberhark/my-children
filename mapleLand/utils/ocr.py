import numpy as np
import cv2
from PIL import ImageGrab
import pytesseract
import time

# pytesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract의 설치 경로에 맞게 조정해야 함

def screen_capture():
    # 전체 화면 캡처
    screen = np.array(ImageGrab.grab(bbox=None))
    # 캡처된 이미지를 회색조로 변환
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return gray_screen

def ocr_processing(image):
    # OCR을 통해 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(image, lang='kor+eng')
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
            print(f"'{target_text}' not found.")
        # 1분 간격으로 반복
        time.sleep(60)

if __name__ == "__main__":
    main()
