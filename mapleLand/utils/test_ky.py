import random
import time

import keyboard

from mapleLand.utils.KeyboardState import KeyboardState

keyboard_state = KeyboardState()


time.sleep(2)
#
# keyboard_state.key_down('f')
# time.sleep(1)
# keyboard_state.key_up('f')

keyboard_state.key_down('right')
time.sleep(0.03)
keyboard_state.key_down('d')
time.sleep(0.3)
keyboard_state.release_all_keys()