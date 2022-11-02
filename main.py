import sys
#from PyQt5.QtWidgets import QApplication, QWidget

import pyautogui
import time

global path
path = './img/'

global crash_dict
global spiral_dict

# 격돌전
# key:현재의 flag , val: 다음 flag
crash_dict = {
    # 미참가(격돌전 돌기)
    'start': ['not_clicked', 'clicked'],
    'not_clicked': 'refresh',
    'clicked': 'refresh',

    'refresh': 'join_battle',
    'join_battle': ['go_battle', 'ok'],

    'go_battle': ['ok', 'battle_result'],
    'ended_battle': 'start',
    'battle_result': ['clear', 'unclear'],

    'clear': 'ok',
    'ok': ['complete', 'clicked'],
    'complete': 'start',

    'unclear': 'start',

    # 종료 (보상 수령)
    'finished': ['no_result', 'result'],
    'no_result': 'start',
    'result': ['end_clear', 'end_ok'],

    'end_clear': 'end_ok',
    'end_ok': 'end_complete',
    'end_complete': ['no_result', 'result'],
}

# 스파이럴 이벤트
spiral_dict = {
    'spiral_go': ['spiral_skill_1', 'spiral_no_ste', 'spiral_battle_result'],

    'spiral_no_ste': 'spiral_no_ste_confirm',
    'spiral_no_ste_confirm': 'spiral_go',

    'spiral_skill_1': 'spiral_skill_2',
    'spiral_skill_2': 'spiral_skill_3',
    'spiral_skill_3': 'spiral_battle_result',


    'spiral_battle_result': 'spiral_clear',
    'spiral_clear': ['spiral_lv_up', 'spiral_retry', 'spiral_new_friend'],
    'spiral_new_friend': ['spiral_retry', 'spiral_new_friend'],
    'spiral_lv_up': 'spiral_clear',
    'spiral_retry': 'spiral_go',



}

# 현재 마우스 좌표
# print(pyautogui.position())

# 스크린샷
# pyautogui.screenshot('1.png', region=(1324, 789, 30, 30))

# Box(left(int), top(int), width(int), height(int))  >> to use .left
# i = pyautogui.locateOnScreen(path+'7.png')


def crash():
    cnt_max = 99999
    cnt = 0
    dic = crash_dict
    flag = "refresh"
    #flag = "finished"

    while cnt < cnt_max:
        print(flag, cnt)

        if flag == 'start':
            cnt += 1
            
            # 20번 마다 보상 수령
            if cnt % 20 == 0:
                flag = 'finished'
            else:
                flag = crash_dict['start']

        if 'refresh' == flag:
            re, flag = search_while(dic, flag, 'not_clicked')
        re, flag = search_while(dic, flag)


def spiral():
    cnt_max = 99999
    cnt = 0
    dic = spiral_dict
    flag = "spiral_go"

    while cnt < cnt_max:
        print(flag, cnt)
        if flag == 'spiral_battle_result':
            cnt += 1

        if 'spiral_clear' in flag:
            re, flag = search_while(dic, flag, 'spiral_retry')
        else:
            re, flag = search_while(dic, flag)


# img를 찾을 때까지 대기한 후 클릭
def search_while(dic, flags, check=None):
    loc = None
    while not loc:
        for flag in flags:
            if type(flags) is str:
                flag = flags

            loc = pyautogui.locateOnScreen(path + flag + '.png', confidence=0.80)

            # 우선으로 찾을 이미지
            if check:
                tmp = pyautogui.locateOnScreen(path + check + '.png', confidence=0.80)
                if tmp:
                    flag = check
                    loc = tmp

            if loc:
                break

    time.sleep(1)
    pyautogui.click(loc)

    return True, dic[flag]


crash()


