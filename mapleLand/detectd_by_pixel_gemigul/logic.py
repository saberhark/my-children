import random
import time

import keyboard


class KeyboardState:
    def __init__(self):
        self.keys = {'left': False,
                     'right': False,
                     'up': False,
                     'down': False,
                     's': False,
                     'd': False,
                     'f': False,
                     'space': False
                     }

    def key_down(self, key):
        if not self.keys[key]:
            keyboard.press(key)
            self.keys[key] = True

    def key_up(self, key):
            keyboard.release(key)
            self.keys[key] = False

    def release_all_keys(self, ignore_keys=None):
        if ignore_keys is None:
            ignore_keys = []
        for key in self.keys:
            if self.keys[key] and key not in ignore_keys:
                keyboard.release(key)
                self.keys[key] = False


keyboard_state = KeyboardState()

# prev_character_pos, positions, state, flag
def move(prev_character_pos, positions, state, flag):
    if positions.get("mini_map_me"):
        mini_map_me = positions.get("mini_map_me")[0]

        if state == flag:
            keyboard_state.release_all_keys(ignore_keys=flag)
            keyboard_state.key_down(flag)

        if mini_map_me[0] < 138:
            state = 'right'
            flag = 'right'
        if mini_map_me[0] > 158:
            state = 'left'
            flag = 'left'

    return prev_character_pos, state, flag


def auto_horn(me, positions, state):
    # 케릭터 좌표 세팅
    if positions.get("me"):
        me = positions["me"][0]
    elif not me:
        return None, None

    result = attack(positions, me)
    print(result, state)
    if result is None:
        return me, state
    elif result != state:
        keyboard_state.key_down(result)
        time.sleep(0.033)
        keyboard_state.key_up(result)
        state = result
    keyboard_state.key_down('f')
    keyboard_state.key_up('f')
    time.sleep(1.3)

    return me, state


def attack(positions, me):
    """ 몬스터가 사거리 내에 있는지 검사 """
    if 'horn' in positions:
        char_x, char_y = me  # 캐릭터의 x, y 좌표
        for zombie_pos in positions['horn']:
            if abs(zombie_pos[0] - char_x) <= 330 and abs(zombie_pos[1] - char_y) <= 200:
                return 'left' if zombie_pos[0] < char_x else 'right'
    return None  # 범위 내 몬스터가 없으면 None 반환


def pause(iterate=1):
    for i in range(iterate):
        random_sleep_time = random.uniform(0.01, 0.03)
        time.sleep(random_sleep_time)


def periodic_key_press():
    while True:
        wait_time = random.randint(1200, 1800)  # 1200초(20분)에서 1800초(30분) 사이의 랜덤한 시간
        time.sleep(wait_time)  # 랜덤한 시간만큼 대기
        keyboard.press_and_release('page down')  # 'Page Down' 키 입력