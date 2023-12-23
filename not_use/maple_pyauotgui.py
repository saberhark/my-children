import keyboard
import time
import pyautogui
import random
import win32api
import win32con

# 85% >> 0.11103153228759766 ~ 0.19905686378479004
# 10% >> 0.319091796875 ~ 0.3030869960784912
#  5% >> 0.4691274166107178
def random_jump_delay():
    weight = random.randrange(1, 100+1)
    if weight <= 85:
        random_delay = random.randrange(19905686378479004 - 11103153228759766)
        random_delay = random_delay + 11103153228759766
        return random_delay / 100000000000000000
    elif weight <= 95:
        random_delay = random.randrange(3190917968751231 - 3030869960784912)
        random_delay = random_delay + 3030869960784912
        return random_delay / 10000000000000000
    else:
        random_delay = random.randrange(4691274166107178 - 4211234325556287)
        random_delay = random_delay + 4211234325556287
        return random_delay / 10000000000000000


# 첫번째 타입 0.08초 근처 / 두번쨰 타입 0.11초 근처로
def key_hold_delay(key=1):
    weight = random.randrange(1, 100+1)
    if key != 1:
        weight += 85
    if weight <= 85:
        random_delay = random.randrange(81432859138747319 - 73721893794328956)
        random_delay = random_delay + 73721893794328956
        return random_delay / 1000000000000000000
    elif weight <= 95:
        random_delay = random.randrange(9637128948384271 - 9237239184320914)
        random_delay = random_delay + 9237239184320914
        return random_delay / 100000000000000000
    else:
        random_delay = random.randrange(1103213789498234 - 1038190432879177)
        random_delay = random_delay + 1038190432879177
        return random_delay / 10000000000000000


def double_jump_hit():
    pyautogui.keyDown('d')
    time.sleep(key_hold_delay())
    pyautogui.keyUp('d')
    time.sleep(random_jump_delay())
    pyautogui.keyDown('d')
    time.sleep(key_hold_delay(2))
    pyautogui.keyUp('d')

    time.sleep(key_hold_delay())
    pyautogui.keyDown('f')
    time.sleep(key_hold_delay())
    pyautogui.keyUp('f')
    time.sleep(key_hold_delay())



def check_double_key_input_delay():
    a = 0
    b = 0
    total = 0
    cnt = 0
    while True:
        if keyboard.read_event() == "d":
            if a == 0:
                a = time.time()
            else:
                b = time.time()
                print(b-a)
                total += b-a
                cnt += 1
                a = 0
                b = 0
        if keyboard.read_key() == "esc":
            print(total/cnt)


def check_key_hold_time():
    KEY = 'a'  # 감지할 키
    DURATION = 0.000001  # 감지할 최소 누른 시간 (단위: 초)

    pressed_time = None
    while True:
        if keyboard.is_pressed(KEY):
            if pressed_time is None:
                pressed_time = time.time()
        else:
            if pressed_time is not None:
                duration = time.time() - pressed_time
                if duration >= DURATION:
                    print(f'{KEY} key was pressed for {duration:.3f} seconds')
                pressed_time = None



def main():
    pyautogui.keyDown('right')
    time.sleep(key_hold_delay())
    for i in range(10):
        double_jump_hit()
        time.sleep(random_jump_delay())
    pyautogui.keyUp('right')
    random_jump_delay

    pyautogui.keyDown('left')
    time.sleep(key_hold_delay())
    for i in range(10):
        double_jump_hit()
        time.sleep(random_jump_delay())
    pyautogui.keyUp('left')
    random_jump_delay


