from macro_utils import *

global path
path = './discord/'


auto_chat_delete = {
    'chat_start': 'mychat',
    'mychat': 'option',
    'option': 'delete',
    'delete': 'delete_confirm',
    'delete_confirm': 'start'
}

# 718 923
def auto_chat():
    cnt = 0
    while True:
        pyautogui.click(find_img(path + 'chat_start.PNG')[0])
        pyautogui.write('...')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.click(718, 923)
        #pyautogui.click(find_img(path + 'mychat.PNG')[0])
        pyautogui.click(find_img(path + 'option.PNG')[0])
        pyautogui.click(find_img(path + 'delete.PNG')[0])
        pyautogui.click(find_img(path + 'delete_confirm.PNG')[0])
        cnt += 1
        print(cnt)
        time.sleep(60)


auto_chat()

