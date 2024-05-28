import tkinter as tk

from PIL import ImageTk, Image
import threading
import logic
import pygetwindow as gw
from datetime import datetime

import time

from mapleLand.utils.detect_colors import detect_colors

# 캔버스와 로그 영역의 크기 설정
canvas_width = 800
canvas_height = 600
log_height = 100

# 사용자가 선택한 영역과 탐지 상태 플래그
selected_area = None
detecting = False
state = 'right'
flag = 'right'
cnt = 0

def get_maplestory_window():
    """ 'MapleStory Worlds-Mapleland' 창의 위치와 크기를 반환하는 함수 """
    try:
        window = gw.getWindowsWithTitle('MapleStory Worlds-Mapleland')[0]
        if window:
            return window.left, window.top, window.width, window.height
    except IndexError:
        print("MapleStory 창을 찾을 수 없습니다.")
        return None


def start_detection():
    """ 색상 탐지를 시작하는 함수 """
    global detecting
    detecting = True
    current_time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    log_text.insert(tk.END, f"Detection started at {current_time}\n")
    log_text.see(tk.END)
    time.sleep(3)


def pause_detection():
    """ 색상 탐지를 일시 정지하는 함수 """
    global detecting
    detecting = False
    current_time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    log_text.insert(tk.END, f"Detection paused at {current_time}\n")
    log_text.see(tk.END)


def update_image():
    global selected_area

    if not selected_area:
        selected_area = get_maplestory_window()

    prev_character_pos = None
    last_frame_time = time.time()
    global state
    global flag
    global cnt
    init = False

    """ 화면을 주기적으로 캡처하고 색상을 감지하는 함수 """
    while True:
        if selected_area and detecting:
            current_time = time.time()
            time_delta = current_time - last_frame_time
            last_frame_time = current_time

            if time_delta > 0:
                fps = 1.0/time_delta
                update_fps_display(fps)

            screenshot, positions = detect_colors(selected_area)

            prev_character_pos, state, flag, cnt = logic.character_move(prev_character_pos, positions, state, flag, cnt)

            if not init:
                screenshot = screenshot.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                update_canvas(screenshot)
                init = True
        else:
            init = False


def update_fps_display(fps):
    # FPS 값을 표시할 라벨 위젯 추가
    # 라벨이 이미 있다면, 값을 업데이트만 합니다.
    fps_label.config(text=f"FPS: {fps:.2f}")


def update_canvas(image):
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image


# 메인 Tkinter 창 설정
root = tk.Tk()
root.title("Color Detection Viewer")
root.geometry(f"{canvas_width}x{canvas_height + log_height}")

# 캔버스와 로그 출력을 위한 프레임 생성
canvas_frame = tk.Frame(root, width=canvas_width, height=canvas_height)
log_frame = tk.Frame(root, width=canvas_width, height=log_height)
canvas_frame.pack()
log_frame.pack()

canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
canvas.pack()

# 로그 출력을 위한 텍스트 위젯
log_text = tk.Text(log_frame, height=5)
log_text.pack()

# 버튼 추가
start_button = tk.Button(log_frame, text="시작", command=start_detection)
pause_button = tk.Button(log_frame, text="일시정지", command=pause_detection)
fps_label = tk.Label(log_frame, text="FPS: 0.00")

start_button.pack(side=tk.LEFT)
pause_button.pack(side=tk.LEFT)
fps_label.pack(side=tk.LEFT)

# 스크린샷 및 업데이트 스레드 시작
thread = threading.Thread(target=update_image, daemon=True)
thread.start()

# 새 스레드에서 periodic_page_down_press 함수 실행
page_down_thread = threading.Thread(target=logic.periodic_key_press, daemon=True)
page_down_thread.start()

root.mainloop()
