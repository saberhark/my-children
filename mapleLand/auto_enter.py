import pyautogui
import time

def press_enter_if_image_appears(image_path):
    location = pyautogui.locateOnScreen(image_path, confidence=0.7)
    if location is not None:
        pyautogui.press('enter')

# 메인 루프
while True:
    #press_enter_if_image_appears('a.png')
    #press_enter_if_image_appears('b.png')
    pyautogui.press('enter')
    time.sleep(0.1)  # CPU 사용을 줄이기 위해 약간의 지연을 추가
