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

    def release_all_keys(self):
        for key in self.keys:
            if self.keys[key]:
                keyboard.release(key)
                self.keys[key] = False


keyboard_state = KeyboardState()


def character_move(me, positions):
    if positions.get("me"):
        me = positions["me"]
    elif not me:
        return

    zombie = positions["zombie"]
    mini_map_me = positions["mini_map_me"]

    return me


# 텔레포트는 오른쪽으로만 씀
def gray_valid_area_teleport(character_pos, gray_positions, teleport):
    # pos와 각 몬스터가 유효 거리내면 TRUE 반환
    pos_x = character_pos[0] + teleport
    pos_y = character_pos[1]

    for pos in gray_positions:
        if pos_x + 180 > pos[0] > pos_x - 50 \
                and pos_y + 150 > pos[1] > pos_y - 50:
            return True
    return False


def gray_valid_area(character_pos, gray_positions):
    # pos와 각 몬스터가 유효 거리내면 TRUE 반환
    pos_x = character_pos[0]
    pos_y = character_pos[1]
    for pos in gray_positions:
        if pos_x + 180 > pos[0] > pos_x - 180 \
                and pos_y + 150 > pos[1] > pos_y - 50:
            return True
    return False


def pause(iterate=1):
    for i in range(iterate):
        random_sleep_time = random.uniform(0.04, 0.06)
        time.sleep(random_sleep_time)


def periodic_key_press():
    while True:
        wait_time = random.randint(1200, 1800)  # 1200초(20분)에서 1800초(30분) 사이의 랜덤한 시간
        time.sleep(wait_time)  # 랜덤한 시간만큼 대기
        keyboard.press_and_release('page down')  # 'Page Down' 키 입력



