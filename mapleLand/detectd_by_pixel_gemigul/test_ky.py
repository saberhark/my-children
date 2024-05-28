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


time.sleep(2)

for i in range(100):
    keyboard_state.key_down('right')
    time.sleep(0.033)
    keyboard_state.key_up('right')
    keyboard_state.key_down('f')
    keyboard_state.key_up('f')
    time.sleep(1.3)
    keyboard_state.key_down('left')
    time.sleep(0.033)
    keyboard_state.key_up('left')
    keyboard_state.key_down('f')
    keyboard_state.key_up('f')
    time.sleep(1.3)