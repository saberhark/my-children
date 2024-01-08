import keyboard


class KeyboardState:
    def __init__(self):
        self.keys = {'left': False,
                     'right': False,
                     'up': False,
                     's': False,
                     'z': False,
                     'f': False,
                     'space': False
                     }

    def key_down(self, key):
        if not self.keys[key]:
            keyboard.press(key)
            self.keys[key] = True

    def key_up(self, key):
        if self.keys[key]:
            keyboard.release(key)
            self.keys[key] = False

    def release_all_keys(self):
        for key in self.keys:
            if self.keys[key]:
                keyboard.release(key)
                self.keys[key] = False


keyboard_state = KeyboardState()


def character_move(selected_area, reference_point, reference_point2, pos, closest_gray, closest_red):
    reference_y = reference_point[1] - selected_area[1]
    reference_x = reference_point2[0] - selected_area[0]

    # 1층에 있는 경우
    if reference_y < pos[1]:
        # 공격 먼저
        if attack(pos, closest_gray, closest_red):
            pass
        elif pos[0] > reference_x:
            keyboard_state.key_up('right')
            keyboard_state.key_down('left')
            keyboard_state.key_down('z')
            keyboard_state.key_up('up')
            if reference_x + 150 > pos[0] > reference_x - 150:
                keyboard_state.key_down('up')
        else:
            keyboard_state.key_up('left')
            keyboard_state.key_down('right')
            keyboard_state.key_down('z')
            keyboard_state.key_up('up')
            if reference_x + 150 > pos[0] > reference_x - 150:
                keyboard_state.key_down('up')

    # 줄을 올라가는 도중 혹은, 2층
    else:
        # 사다리에 있다고 판단
        if reference_x + 20 > pos[0] > reference_x:
            keyboard_state.key_up('left')
            keyboard_state.key_up('s')
            keyboard_state.key_up('f')
            keyboard_state.key_down('z')
            keyboard_state.key_down('up')
            keyboard_state.key_down('right')
        else:
            # 공격 먼저
            if attack(pos, closest_gray, closest_red):
                pass
            else:
                keyboard_state.key_up('left')
                keyboard_state.key_up('up')
                keyboard_state.key_down('z')
                keyboard_state.key_down('right')


# 공격하면 True 리턴
def attack(pos, closest_gray, closest_red):
    # 선 루팡
    if gray_valid_area(pos, closest_gray):
        keyboard_state.release_all_keys()
        keyboard_state.key_down('f')
    # 후 커즈
    elif red_valid_area(pos, closest_red):
        keyboard_state.release_all_keys()

        if closest_red[0] > pos[0]:
            keyboard_state.key_down('right')
        else:
            keyboard_state.key_down('left')
        keyboard_state.key_down('s')
    else:
        keyboard_state.key_up('f')
        keyboard_state.key_up('s')
        return False

    return True



def gray_valid_area(pos, closest_gray):
    # pos와 각 몬스터가 유효 거리내면 TRUE 반환
    pos_x = pos[0]
    pos_y = pos[1]

    if not closest_gray:
        return False
    if pos_x + 200 > closest_gray[0] > pos_x - 200 and pos_y + 100 > closest_gray[1] > pos_y - 100:
        return True
    return False


def red_valid_area(pos, closest_red):
    # pos와 각 몬스터가 유효 거리내면 TRUE 반환
    pos_x = pos[0]
    pos_y = pos[1]

    if not closest_red:
        return False
    if pos_x + 300 > closest_red[0] > pos_x - 300 and pos_y + 100 > closest_red[1] > pos_y - 100:
        return True
    return False
