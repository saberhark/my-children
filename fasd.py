import time
import pyautogui

loc = (0, 0)
cnt = 0

while True:
    loc = (313, 517)
    pyautogui.click(loc)
    loc = (1083, 558)
    pyautogui.click(loc)

    time.sleep(0.3)
    loc = (1088, 539)
    pyautogui.click(loc)
    print(cnt)

