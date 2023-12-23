# https://yungyikim-blog.tistory.com/entry/Python-Keyboard-Hook-Example

import sys
import win32api, win32con
from ctypes import *
from ctypes.wintypes import DWORD, HHOOK, HINSTANCE, MSG, WPARAM, LPARAM

# 입력할 문자열
input_string = 'Hello, world!'

user32 = windll.user32
kernel32 = windll.kernel32

class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ('vkCode', DWORD),
        ('scanCode', DWORD),
        ('flags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', DWORD)]



def installHookProc(hooked, pointer):
    hooked = user32.SetWindowsHookExA(
        13,
        pointer,
        None,
        0
    )
    print ('hooked:', hooked)
    if not hooked:
        return False
    return True




# 하드웨어 인풋 후킹 처리를 위한 콜백 함수
def keyboard_hook_proc(nCode, wParam, lParam):
    # wParam 값이 0x100인 경우, 키가 눌렸음을 나타냅니다.
    if wParam == 0x100:
        # lParam에서 가상 키 코드와 스캔 코드를 추출합니다.
        vk_code = lParam & 0xff
        scan_code = (lParam >> 16) & 0xff

        # 추출한 가상 키 코드와 스캔 코드를 이용하여 키보드 메시지를 보냅니다.
        win32api.keybd_event(vk_code, scan_code, 0, 0)

    # 다음 후킹 처리를 계속합니다.
    return win32con.CallNextHookEx(None, nCode, wParam, lParam)

HOOKPROTYPE = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
pointer = HOOKPROTYPE(keyboard_hook_proc)

# 키보드 후킹을 등록합니다.
keyboard_hook = user32.SetWindowsHookExA(
    13,
    pointer,
    None,
    0)

# 메시지 루프를 시작합니다.
while True:
    # 하드웨어 인풋을 대기합니다.
    # 이 부분은 하드웨어 인풋을 받아오는 코드로 대체해야 합니다.
    input_char = input()

    # 하드웨어 인풋이 '1'인 경우, 문자열을 입력합니다.
    if input_char == '1':
        for char in input_string:
            # 문자열의 각 문자에 대해 키보드 메시지를 보냅니다.
            vk_code = ord(char)
            scan_code = win32api.MapVirtualKey(vk_code, 0)
            win32api.keybd_event(vk_code, scan_code, 0, 0)

    # 하드웨어 인풋이 '2'인 경우, 프로그램을 종료합니다.
    elif input_char == '2':
        break

# 키보드 후킹을 해제합니다.
win32api.UnhookWindowsHookEx(keyboard_hook)