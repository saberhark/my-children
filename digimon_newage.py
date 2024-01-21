import sys
import pyautogui
import time
from macro_utils import *

global path
path = './new_age/'


def real_time_pvp(derank=False):
    print("실시간 대전 시작")
    cnt = 1;
    while True:
        # ai 전투
        print("반복 횟수 >>", cnt);
        loc = find_img(path+'realtime_pvp.png')[0]
        time.sleep(1)
        pyautogui.click(loc)

        if(derank):
            loc = find_img(path + 'setting.png', confidence=0.8)[0]
            time.sleep(1)
            pyautogui.click(loc)

            loc = find_img(path + 'surrend.png', confidence=0.8)[0]
            time.sleep(1)
            pyautogui.click(loc)

        else:
            loc = find_img(path + 'realtime_auto.png', confidence=0.5)[0]
            time.sleep(4)
            pyautogui.click(loc)

        find_img(path + 'end_realtime.png')[0]
        print('end')
        time.sleep(1)
        pyautogui.click(900, 530)


        cnt = cnt+1


def one_pvp(total=10, skip=0, next=False, three_total=10, three_skip=0):
    print("1:1 시작")
    while total > skip:
        print("남은 횟수 >>", total, 'skip >>', skip)
        # 유저 목록중 가장 오른쪽부터 skip해서 클릭
        pyautogui.click(find_img(path+'one_pvp_select_user.png', reverse=True)[skip])
        pyautogui.click(find_img(path + 'one_pvp_start.png')[0])

        # 전투 진입 시 스킵
        pyautogui.click(find_img(path + 'one_pvp_skip.png', confidence=0.8)[0])

        # 전투 종료
        if len(find_img(path + 'one_pvp_end.png')) > 0:
            pyautogui.click((735, 450))
            total -= 1

    pyautogui.click(find_img(path + 'one_pvp_back.png', confidence=0.8)[0])

    # 33 대전 실행
    if next:
        pyautogui.click(find_img(path + 'three_pvp_enter.png')[0])
        three_pvp(three_total, three_skip)


def three_pvp(total=10, skip=0):
    print("3:3 대전 시작")
    while total > skip:
        print("남은 횟수 >>", total, 'skip >>', skip)
        # 유저 목록중 가장 오른쪽부터 skip해서 클릭
        pyautogui.click(find_img(path + 'one_pvp_select_user.png', reverse=True)[skip])
        pyautogui.click(find_img(path + 'three_pvp_start.png')[0])

        # 전투 진입 시 스킵
        pyautogui.click(find_img(path + 'three_pvp_skip.png', confidence=0.8)[0])
        pyautogui.click(find_img(path + 'three_pvp_skip2.png')[0])


        # 전투 종료
        if len(find_img(path + 'three_pvp_end.png')) > 0:
            pyautogui.click((735, 450))
            total = total - 1


def capsule():
    while True:
        start_btn1 = find_img(path + "capsule_start1.PNG")[0]
        time.sleep(3)
        pyautogui.click(start_btn1)

        start_btn2 = find_img(path + "capsule_start2.PNG", confidence=0.5)[0]
        time.sleep(1)
        pyautogui.click(start_btn2)

        end_btn = find_img(path + "capsule_end.PNG", confidence=0.8)[0]
        time.sleep(1)
        pyautogui.click(900, 720)

        #end_btn2 = find_img(path + "capsule_end2.PNG", confidence=0.8)[0]
        time.sleep(6)
        pyautogui.click(900, 720)


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

        loc = find_img(path + 'story_skip.png', confidence=0.5)[0]
        time.sleep(1)
        pyautogui.click(loc)

        loc = None
        while loc is None:
            skip = pyautogui.locateOnScreen(path + 'story_skip.png', confidence=0.5)
            if skip is not None:
                pyautogui.click(skip)

            loc = pyautogui.locateOnScreen(path + 'story_end.png', confidence=0.8)

        time.sleep(1)
        pyautogui.click(loc)

        print('반복 횟수  >>', cnt)

def coop():
    while True:
        click_img2(path + "coop_start.PNG")
        click_img2(path + "one_pvp_skip.PNG", confidence=0.8)
        click_img2(path + "story_end.PNG", confidence=0.8)



def coop1():
    while True:
        click_img2(path + "story_start2.PNG")
        click_img2(path + "story_skip.PNG", confidence=0.8)
        click_img2(path + "event_start.PNG", confidence=0.8)

        loc = pyautogui.locateOnScreen(path + 'capsule_end.png', confidence=0.8)
        if loc:
            pyautogui.click(900, 720)




real_time_pvp()
#real_time_pvp(True)
#story()
#capsule()

#coop()
#coop1()
#one_pvp(next=True)
#three_pvp(total=8)
