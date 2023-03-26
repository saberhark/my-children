import time
import random
import win32api
import win32con


scan_code = {
    "ESC"	:1,
    "1"	:2,
    "2"	:3,
    "3"	:4,
    "4"	:5,
    "5"	:6,
    "6"	:7,
    "7"	:8,
    "8"	:9,
    "9"	:10,
    "0"	:11,
    "-"	:12,
    "="	:13,
    "BACK"	:14,
    "TAB"	:15,
    "Q"	:16,
    "W"	:17,
    "E"	:18,
    "R"	:19,
    "T"	:20,
    "Y"	:21,
    "U"	:22,
    "I"	:23,
    "O"	:24,
    "P"	:25,
    "["	:26,
    "]"	:27,
    "ENTER"	:28,
    "LCTRL"	:29,
    "A"	:30,
    "S"	:31,
    "D"	:32,
    "F"	:33,
    "G"	:34,
    "H"	:35,
    "J"	:36,
    "K"	:37,
    "L"	:38,
    ";"	:39,
    "'"	:40,
    "`"	:41,
    "LSHIFT"	:42,

    "Z"	:44,
    "X"	:45,
    "C"	:46,
    "V"	:47,
    "B"	:48,
    "N"	:49,
    "M"	:50,

    "RSHIFT"	:54,
    "PRTSCR"	:55,
    "LALT"	:56,
    "SPACE"	:57,
    "CAPS"	:58,
    "F1"	:59,
    "F2"	:60,
    "F3"	:61,
    "F4"	:62,
    "F5"	:63,
    "F6"	:64,
    "F7"	:65,
    "F8"	:66,
    "F9"	:67,
    "F10"	:68,
    "NUM"	:69,
    "SCROLL"	:70,
    "HOME"	:71,
    "UP"	:72,
    "PGUP"	:73,
    "LEFT"	:75,
    "5"	:76,
    "RIGHT"	:77,
    "END"	:79,
    "DOWN"	:80}

#0.001
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
    key_down_ext(scan_code["D"])
    time.sleep(key_hold_delay())
    key_up_ext(scan_code["D"])
    time.sleep(random_jump_delay())
    key_down_ext(scan_code["D"])
    time.sleep(key_hold_delay(2))
    key_up_ext(scan_code["D"])

    time.sleep(key_hold_delay())
    key_down_ext(scan_code["F"])
    time.sleep(key_hold_delay())
    key_up_ext(scan_code["F"])
    time.sleep(key_hold_delay())


def key_down_ext(scan_code):
    win32api.keybd_event(0, scan_code, win32con.KEYEVENTF_SCANCODE, 0)


def key_up_ext(scan_code):
    win32api.keybd_event(0, scan_code, win32con.KEYEVENTF_SCANCODE | win32con.KEYEVENTF_KEYUP, 0)


def main():
    key_down_ext(scan_code["RIGHT"])
    time.sleep(key_hold_delay())
    for i in range(5):
        double_jump_hit()
        time.sleep(random_jump_delay())
    key_up_ext(scan_code["RIGHT"])
    random_jump_delay

    key_down_ext(scan_code["LEFT"])
    time.sleep(key_hold_delay())
    for i in range(5):
        double_jump_hit()
        time.sleep(random_jump_delay())
    key_up_ext(scan_code["LEFT"])
    random_jump_delay


if __name__ == '__main__':
    main()

