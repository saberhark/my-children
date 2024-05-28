import random
import time

import keyboard

from mapleLand.utils.KeyboardState import KeyboardState

keyboard_state = KeyboardState()


# 1층 2층
def character_move(me, positions, state, flag, cnt):
    mini_map_me = positions["mini_map_me"][0]

    x_coord = mini_map_me[0]
    y_coord = mini_map_me[1]

    # 케릭터 좌표 세팅
    if positions.get("me"):
        me = positions["me"][0]
    elif not me:
        return me, state, flag, cnt

    result = magic_claw(positions, me)
    if result:
        me, state = attack(me, result)
        return me, state, flag, cnt

    if x_coord < 40 and flag != 'right':
        flag = 'right'
        cnt += 1
    elif x_coord > 160 and flag != 'left':
        flag = 'left'
        cnt += 1
    state = flag

    keyboard_state.key_down(flag)
    if 40 < x_coord < 55 and 100 < y_coord:
        time.sleep(0.03)
        keyboard_state.key_down('d')
    elif 113 < x_coord < 119 and 96 < y_coord:
        keyboard_state.release_all_keys()
        keyboard_state.key_down('d')
    else:
        keyboard_state.release_all_keys(ignore_keys=flag)



    return me, state, flag, cnt


def attack(me, result):
    keyboard_state.release_all_keys(ignore_keys=result)
    keyboard_state.key_down(result)
    time.sleep(0.033)
    keyboard_state.key_down('f')
    time.sleep(1)
    keyboard_state.release_all_keys()
    time.sleep(0.5)

    state = result

    return me, state


def magic_claw(positions, me):
    """ 몬스터가 사거리 내에 있는지 검사 """
    if 'bear' in positions:
        char_x, char_y = me  # 캐릭터의 x, y 좌표
        for monster in positions['bear']:
            if abs(monster[0] - char_x) <= 330 and abs(monster[1] - char_y) <= 50:
                return 'left' if monster[0] < char_x else 'right'
    return None  # 범위 내 몬스터가 없으면 None 반환


def periodic_key_press():
    while True:
        wait_time = random.randint(1200, 1800)  # 1200초(20분)에서 1800초(30분) 사이의 랜덤한 시간
        time.sleep(wait_time)  # 랜덤한 시간만큼 대기
        keyboard.press_and_release('page down')  # 'Page Down' 키 입력