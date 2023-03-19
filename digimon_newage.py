import sys
import pyautogui
import time
from macro_utils import *

global path
path = './new_age/'


def real_time_pvp():
    print("실시간 대전 시작")
    cnt = 1;
    while True:
        # ai 전투
        print("반복 횟수 >>", cnt);
        loc = find_img(path+'realtime_pvp.png')[0]
        time.sleep(2)
        pyautogui.click(loc)

        print('end')
        find_img(path + 'end_realtime.png')
        time.sleep(1)
        pyautogui.click((378, 517))
        cnt = cnt+1


def one_pvp(total=10, skip=0, next=False, three_total=10, three_skip=0):
    print("1:1 시작")
    while total > skip:
        print("남은 횟수 >>", total, 'skip >>', skip)
        # 유저 목록중 가장 오른쪽부터 skip해서 클릭
        pyautogui.click(find_img(path+'one_pvp_select_user.png', reverse=True)[skip])
        pyautogui.click(find_img(path + 'one_pvp_start.png')[0])

        # 전투 진입 시 스킵
        if len(find_img(path+'magnummon.png')) > 0:
            pyautogui.click((229, 350))

        # 전투 종료
        if len(find_img(path + 'one_pvp_end.png')) > 0:
            pyautogui.click((487, 577))
            total -= 1

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
        while True:
            time.sleep(1)
            pyautogui.click((266, 350))
            loc = pyautogui.locateOnScreen(path + 'three_pvp_skip.png', confidence=0.80)
            if loc:
                pyautogui.click(loc)
                break

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


def dark_area():
    cnt = 0
    while True:
        cnt += 1
        pyautogui.click(find_img(path + 'dark_area_next.png', reverse=True)[0])
        print('반복 횟수 >>', cnt)
        time.sleep(5)


def story():
    cnt = 0
    while True:
        cnt += 1
        loc = find_img(path+'story_start.png')[0]
        time.sleep(1)
        pyautogui.click(loc)
        time.sleep(1)
        loc = find_img(path+'story_start2.png')[0]
        pyautogui.click(loc)

        loc = None
        while loc is None:
            pyautogui.click((886,350))
            time.sleep(1)
            loc = pyautogui.locateOnScreen(path + 'story_end.png')
        time.sleep(1)
        pyautogui.click(loc)
        print('반복 횟수  >>', cnt)