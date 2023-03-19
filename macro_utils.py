import time
import pyautogui


# 이미지 찾을 때까지 찾은 후 좌표 반환
def find_img(img_path, confidence=0.9, reverse=False):
    print("searching file >>", img_path)
    while True:
        find_arr = [i for i in pyautogui.locateAllOnScreen(img_path, confidence=confidence)]
        if len(find_arr) > 0:
            if reverse:
                return find_arr[::-1]
            else:
                return find_arr
        time.sleep(1)


def click_img(img_path, confidence=0.9):
    while True:
        find_arr = pyautogui.locateOnScreen(img_path, confidence=confidence)
        if find_arr:
            return find_arr
        time.sleep(1)


# img를 찾을 때까지 대기한 후 클릭
def search_with_dict(path, dic, flags, check=None):
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