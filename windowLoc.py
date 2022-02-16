"""
창의 좌표(xywh)를 구하고 지정 구역안에서만 img를 search하게함
"""


import time
import mouse
import pyautogui


cur = mouse.get_position()
pyautogui.click(100, 100)
mouse.move(cur[0], cur[1])

print(pyautogui.getAllWindows)
print(pyautogui.mouseInfo())


def window_locate():
    click = 0
    pos = [0]*2

    while click < 2:
        if mouse.is_pressed("left"):
            pos[click] = mouse.get_position()
            click += 1
            print(click, '번쨰 :', pos)
        time.sleep(0.1)

    result = pos[0][0], pos[0][1], pos[1][0] - pos[0][0], pos[1][1] - pos[0][1]
    print('xywh : ', result)

    return result

loc = None
while not loc:
    try:
        loc = pyautogui.locateOnScreen('img/7.png', confidence=0.80, region = window_locate())
    except:
        print("좌표 제대로")

time.sleep(1)
pyautogui.click(loc)
