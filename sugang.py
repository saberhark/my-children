from macro_utils import *

global path
path = './sugang/'



# 718 923
def auto_chat():
    cnt = 0
    while True:
        pyautogui.click(find_img(path + '1.PNG')[0])
        pyautogui.click(find_img(path + '2.PNG')[0])
        pyautogui.click(find_img(path + '3.PNG')[0])
        cnt += 1
        print(cnt)


auto_chat()

