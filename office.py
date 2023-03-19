import pyautogui
import time


def time_now(add_time=0):
    now = time.localtime(time.time() + add_time)
    weekday = list("월화수목금토일")

    return f"{now.tm_year}년 {now.tm_mon}월 {now.tm_mday}일 {weekday[now.tm_wday]}요일 {now.tm_hour}시 {now.tm_min}분 {now.tm_sec}초"


def auto_check_out(hours=0, mins=0, secs=0):
    loc = (853, 716)

    add_time = hours*60*60 + mins*60 + secs

    # test
    time.sleep(2)
    pyautogui.click(loc)
    pyautogui.click(loc)
    time.sleep(2)
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')

    print(f"Start time >> {time_now()}")
    print(f"Predict end time >> {time_now(add_time)}")

    # main
    time.sleep(add_time)
    pyautogui.click(loc)
    pyautogui.click(loc)
    time.sleep(5)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

    print(f"End time >> {time_now()}")


# 현재 마우스 좌표
# print(pyautogui.position())
auto_check_out(hours=1, mins=33, secs=0)
