import pyautogui
import time

cnt = 34

while cnt >0:
    cnt -=1
    # 클릭할 좌표들을 리스트로 정의
    click_points = [
        (712, 513),
        (861, 629),
        (1354, 593),
        (1315, 699)
    ]

    # 휠다운 후 클릭할 좌표들을 리스트로 정의
    wheel_down_click_points = [
        (950, 378),
        (950, 378),
        (1305, 695),
        (1374, 589)
    ]

    # 첫 번째 좌표들을 클릭
    for point in click_points:
        pyautogui.click(point)
        time.sleep(0.5)  # 클릭 사이에 약간의 지연을 줍니다.

    time.sleep(2)
    # 휠 다운 수행
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    # 휠 다운 수행
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.
    pyautogui.scroll(-500)  # 이 값은 환경에 따라 조정할 수 있습니다.

    # 휠다운 후 클릭할 좌표들을 클릭
    for point in wheel_down_click_points:
        pyautogui.click(point)
        time.sleep(0.5)  # 클릭 사이에 약간의 지연을 줍니다.
