import sys
# from PyQt5.QtWidgets import QApplication, QWidget

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
    'spiral_lv_up': 'spiral_clear',
    'spiral_retry': 'spiral_go',

}
loc = 313

tmp = pyautogui.locateOnScreen(path + 'spiral_new_friend' + '.png', confidence=0.80)
loc = tmp if tmp else loc
print(loc)


