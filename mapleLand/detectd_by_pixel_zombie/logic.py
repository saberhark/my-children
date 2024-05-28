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


# 1층 2층
def character_move(me, positions, flag):
    mini_map_me = positions["mini_map_me"][0]
    print(mini_map_me, flag)
    x_coord = mini_map_me[0]
    y_coord = mini_map_me[1]

    # 케릭터 좌표 세팅
    if positions.get("me"):
        me = positions["me"][0]
    elif not me:
        return me, flag

    if attack(positions, me):
        keyboard_state.release_all_keys(['f', 'up'])
        pause()
        keyboard_state.key_down('f')

        return me, flag

    # 2층 가야됨
    if flag:
        if 100 < x_coord and y_coord < 164:
            flag = False
            return me, flag

        if 100 <= x_coord <= 114:
            keyboard_state.release_all_keys(['right', 'up'])
            pause()
            keyboard_state.key_down('right')
            pause()
            keyboard_state.key_down('up')
            pause()
            return me, flag
        elif 114 < x_coord < 136:
            keyboard_state.release_all_keys(['left', 'up'])
            pause()
            keyboard_state.key_down('left')
            pause()
            keyboard_state.key_down('up')
            pause()
            return me, flag
        elif 136 <= x_coord:
            keyboard_state.release_all_keys(['left', 'up'])
            pause()
            keyboard_state.key_down('left')
            pause()
            keyboard_state.key_down('space')
            pause()
            keyboard_state.key_down('up')
            pause()
            return me, flag
    # 3층 꼭대기 (리젠되는곳)
    if y_coord < 150 and x_coord < 100:
        jump_down()
        flag = True

    # 중간층
    elif 176 < y_coord < 180 and x_coord < 100:
        jump_down()
        keyboard_state.key_down('f')
        time.sleep(0.5)
        pause()

    # 2층
    elif 160 < y_coord < 170:
        if x_coord < 170:
            keyboard_state.release_all_keys(['right', 'space'])
            pause()
            keyboard_state.key_down('right')
            keyboard_state.key_down('space')
        # 왼쪽으로 잠깐 왔다가 밑으로 점프
        else:
            keyboard_state.key_up('right')
            pause()
            keyboard_state.key_down('left')
            pause()
            keyboard_state.key_down('space')
            time.sleep(1)
            pause()
            keyboard_state.key_down('down')
            pause()
            keyboard_state.key_down('d')
            pause()
            time.sleep(1.2)


    # 1층 (바닥)
    elif 190 < y_coord:
        if x_coord > 200:
            keyboard_state.key_up('f')
        keyboard_state.release_all_keys(['right', 'space', 'f'])
        pause()
        #if x_coord <200:
        #    keyboard_state.key_down('f')
        #    pause()
        keyboard_state.key_down('right')
        pause()
        keyboard_state.key_down('space')
        pause()
        time.sleep(0.5)
        pause()

    return me, flag


'''
2층만
x: 96 ~ 191
y: 163 ~ 168

밧줄 x : 114, 175
'''
def character_move_2f(me, positions, state):
    mini_map_me = positions["mini_map_me"][0]
    print(mini_map_me)

    # 케릭터 좌표 세팅
    if positions.get("me"):
        me = positions["me"][0]
    elif not me:
        return None, None

    # x 좌표
    x_coord = mini_map_me[0]

    if attack(positions, me):
        keyboard_state.release_all_keys()
        pause()
        keyboard_state.key_down('f')
        time.sleep(0.25)
        pause()
        keyboard_state.release_all_keys()
        pause()

        return me, state

    # 114에 도착했거나 더 왼쪽에 있을 경우, 오른쪽으로 이동해야 함
    if x_coord <= 114 and state != 'right':
        state = 'right'
        keyboard_state.key_up('left')
        pause()
        keyboard_state.key_down('right')

    # 175에 도착했거나 더 오른쪽에 있을 경우, 왼쪽으로 이동해야 함
    elif x_coord >= 175 and state != 'left':
        state = 'left'
        keyboard_state.key_up('right')
        pause()
        keyboard_state.key_down('left')

    # 현재 상태에 따라 캐릭터 움직임 결정
    else:
        if state == 'right':
            keyboard_state.key_up('left')
            pause()
            keyboard_state.key_down('right')
        elif state == 'left':
            keyboard_state.key_up('right')
            pause()
            keyboard_state.key_down('left')
    return me, state


def attack(positions, me):
    """좀비가 캐릭터와 x 좌표 기준으로 180 이내에 있는지 검사하는 함수"""
    if 'zombie' in positions:
        char_x = me[0]  # 캐릭터의 x 좌표
        char_y = me[1]  # 캐릭터의 x 좌표
        for zombie_pos in positions['zombie']:
            if abs(zombie_pos[0] - char_x) <= 150 and abs(zombie_pos[1] - char_y) <= 130:
                return True
    return False


# 밧줄타기
def move_up(direction, x_coord):
    # 114와 175와의 거리 계산
    distance_to_114 = abs(114 - x_coord)
    distance_to_175 = abs(175 - x_coord)
    direction = None

    if distance_to_114 <= distance_to_175 and x_coord >= 114:
        direction = "left"
        state = "left_lope"
    elif distance_to_114 <= distance_to_175 and x_coord <= 114:
        direction = "right"
        state = "right_lope"
    elif distance_to_114 >= distance_to_175 and x_coord >= 175:
        direction = "left"
        state = "left_lope"
    elif distance_to_114 >= distance_to_175 and x_coord <= 175:
        direction = "right"
        state = "right_lope"

    keyboard_state.release_all_keys()
    pause()
    keyboard_state.key_down(direction)
    pause()
    keyboard_state.key_down("up")
    pause()
    return


# 밑점
def jump_down():
    keyboard_state.release_all_keys()
    pause()
    keyboard_state.key_down("left")
    pause()
    keyboard_state.key_down("down")
    pause()
    keyboard_state.key_down("d")
    time.sleep(0.9)
    pause()
    keyboard_state.release_all_keys()


# 움직이면서 힐
def jump_heal(direction):
    keyboard_state.release_all_keys()
    pause()
    keyboard_state.key_down(direction)
    pause()
    keyboard_state.key_down("d")
    pause()
    keyboard_state.key_down("f")
    pause()
    keyboard_state.release_all_keys()
    time.sleep(0.5)
    pause()


# 힐 텔포
def teleport_heal(direction):
    keyboard_state.release_all_keys()
    pause()
    keyboard_state.key_down(direction)
    pause()
    keyboard_state.key_down("space")
    pause()
    keyboard_state.key_down("f")
    pause()
    keyboard_state.release_all_keys()
    time.sleep(0.5)
    pause()


def pause(iterate=1):
    for i in range(iterate):
        random_sleep_time = random.uniform(0.01, 0.03)
        time.sleep(random_sleep_time)


def periodic_key_press():
    while True:
        wait_time = random.randint(1200, 1800)  # 1200초(20분)에서 1800초(30분) 사이의 랜덤한 시간
        time.sleep(wait_time)  # 랜덤한 시간만큼 대기
        keyboard.press_and_release('page down')  # 'Page Down' 키 입력



