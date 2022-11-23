import sys
import pyautogui
import time
from macro_utils import *

global path
path = './new_age/'


def real_time_pvp():
    while True:
        realtime_pvp = pyautogui.locateOnScreen(path + 'realtime_pvp.png', confidence=0.80)
        ai_auto = pyautogui.locateOnScreen(path + 'ai_auto.png', confidence=0.80)
        end_realtime = pyautogui.locateOnScreen(path + 'end_realtime.png', confidence=0.80)

        if realtime_pvp:
            pyautogui.click(realtime_pvp)
            time.sleep(2)
        if ai_auto:
            pyautogui.click(ai_auto)
            time.sleep(2)
        if end_realtime:
            pyautogui.click((378, 517))
            time.sleep(2)

def one_pvp(total=10, skip=0, next=False, three_total=10, three_skip=0):
    print("1:1 시작")
    while total > skip:
        print("남은 횟수 >>", total, 'skip >>', skip)
        # 유저 목록중 가장 오른쪽부터 skip해서 클릭
        pyautogui.click(find_img(path+'one_pvp_select_user.png', reverse=True)[skip])
        pyautogui.click(find_img(path + 'one_pvp_start.png')[0])

        # 전투 진입 시 스킵
        if len(find_img(path+'dunacemon.png')) > 0:
            pyautogui.click((229, 350))

        # 전투 종료
        if len(find_img(path + 'one_pvp_end.png')) > 0:
            pyautogui.click((487, 577))
            total = total -1
    # 33 대전 실행
    if next:
        if len(find_img(path+'one_pvp_wait.png')) > 0:
            pyautogui.click((79, 347))  # go back
        pyautogui.click(find_img(path + 'three_pvp_enter.png')[0])
        three_pvp(three_total, three_skip)


def three_pvp(total=10, skip=0):
    print("3:3 대전 시작")
    while total > skip:
        print("남은 횟수 >>", total, 'skip >>', skip)
        # 유저 목록중 가장 오른쪽부터 skip해서 클릭
        pyautogui.click(find_img(path + 'three_pvp_select_user.png', reverse=True)[skip])
        pyautogui.click(find_img(path + 'three_pvp_start.png')[0])

        # 전투 진입 시 스킵
        if len(find_img(path + 'dunacemon.png')) > 0:
            pyautogui.click((266, 350))
            pyautogui.click(find_img(path + 'three_pvp_skip.png')[0])

        # 전투 종료
        if len(find_img(path + 'three_pvp_end.png')) > 0:
            pyautogui.click((487, 577))
            total = total - 1


def capsule():
    while True:
        start_btn1=pyautogui.locateOnScreen(path + 'capsule_start1.PNG', confidence=0.80)
        end_btn=pyautogui.locateOnScreen(path + 'capsule_end.PNG', confidence=0.80)
        if start_btn1:
            pyautogui.click(start_btn1)
            time.sleep(5)
            pyautogui.click((822,748))
        if end_btn:
            pyautogui.click(end_btn)
            time.sleep(10)
            pyautogui.click((481, 638))



one_pvp(total=0, next=True, three_total=5)