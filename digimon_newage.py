import sys
#from PyQt5.QtWidgets import QApplication, QWidget

import pyautogui
import time

global path
path = './new_age/'

while True:
    realtime_pvp = pyautogui.locateOnScreen(path + 'realtime_pvp.png', confidence=0.80)
    ai_auto = pyautogui.locateOnScreen(path + 'ai_auto.png', confidence=0.80)
    end_realtime = pyautogui.locateOnScreen(path + 'end_realtime.png', confidence=0.80)

    if realtime_pvp:
        pyautogui.click(realtime_pvp)
        time.sleep(2)
    if ai_auto:
        pyautogui.click(ai_auto)
        time.sleep(2)
    if end_realtime:
        pyautogui.click((378, 517))
        time.sleep(2)

