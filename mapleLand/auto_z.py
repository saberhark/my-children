import pyautogui
import keyboard
import time

def is_f2_pressed():
    return keyboard.is_pressed('F2')

while not is_f2_pressed():
    pyautogui.press('z')
    time.sleep(0.1)