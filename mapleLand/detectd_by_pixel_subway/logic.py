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


def character_move(character_pos, gray_positions, right_flag, left_flag, middle_flag, mini_map_me, mini_map_portal):
    print(mini_map_me)
    if left_flag:
        # 왼쪽에서 오른쪽으로 감
        keyboard_state.key_up('left')
        keyboard_state.key_down('right')

        # 오른쪽 끝 도착
        if mini_map_me[0] > 244:
            print("오른쪽 도착")
            keyboard_state.release_all_keys()
            pause()
            keyboard_state.key_down('left')
            keyboard_state.key_down('space')
            pause(2)
            right_flag = True
            left_flag = False

        # 몬스터 있을 시 순간이동+공격
        if gray_valid_area_teleport(character_pos, gray_positions, 120):
            keyboard_state.key_down('space')
            pause()
            keyboard_state.key_down('f')
            pause(4)
        else:
            keyboard_state.key_up('space')
            keyboard_state.key_up('f')

    # 오른쪽에서 왼쪽으로
    elif right_flag:
        # 근처에 몬스터 있을 시 공격
        if gray_valid_area(character_pos, gray_positions):
            keyboard_state.release_all_keys()
            keyboard_state.key_down('f')
            pause(8)
            return right_flag, left_flag, middle_flag
        else:
            keyboard_state.key_up('f')

        if middle_flag:
            keyboard_state.key_up('up')
            keyboard_state.key_up('space')
            keyboard_state.key_up('down')
            keyboard_state.key_up('d')
            keyboard_state.key_down('left')

            if mini_map_portal:
                if mini_map_portal[0]+120 < mini_map_me[0] < mini_map_portal[0] + 130 \
                        and 170 < mini_map_me[1] < 178:
                    print("중간")
                    keyboard_state.key_up('left')
                    pause()
                    keyboard_state.key_down('up')
                    keyboard_state.key_down('space')
                    pause()
                elif 84 < mini_map_me[0] < 91 and 170 < mini_map_me[1] < 176:
                    keyboard_state.key_up('left')
                    pause()
                    keyboard_state.key_down('up')
                    keyboard_state.key_down('space')
                    pause()
                elif mini_map_me[1] < 170 and mini_map_me[0] < 72:
                    keyboard_state.key_down('down')
                    keyboard_state.key_down('d')

        else:
            # 3층
            if mini_map_me[1] < 170:
                keyboard_state.key_up('up')
                keyboard_state.key_up('space')
                keyboard_state.key_down('left')
                if mini_map_me[0] < 170:
                    middle_flag = True

            # 3층 아닐 때
            else:
                if 215 < mini_map_me[0]:
                    keyboard_state.key_up('right')
                    keyboard_state.key_up('space')
                    keyboard_state.key_down('left')

                elif mini_map_me[0] < 209:
                    keyboard_state.key_up('left')
                    keyboard_state.key_up('space')
                    keyboard_state.key_down('right')
                else:
                    keyboard_state.release_all_keys()
                    pause()
                    keyboard_state.key_down('up')
                    keyboard_state.key_down('space')
                    pause()

        # 왼쪽 끝 도착
        if mini_map_me[0] < 62 and mini_map_me[1]>186:
            keyboard_state.release_all_keys()
            keyboard_state.key_down('f')
            keyboard_state.key_down('right')
            right_flag = False
            left_flag = True
            middle_flag = False

    return right_flag, left_flag, middle_flag


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



