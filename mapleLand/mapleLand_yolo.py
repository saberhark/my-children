'''
conda env list
activate yolov5-new
python ../mapleLand/mapleLand_yolo.py

python train.py --img 640 --batch 8 --epochs 100 --data my_dataset.yaml --weights yolov5s.pt --cache
python train.py --img 640 --batch 8 --epochs 200 --data my_dataset.yaml --weights yolov5s.pt --cache --save-period 50

'''


import tkinter as tk
from PIL import Image, ImageTk, ImageGrab

import detection
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

# 전역 변수로 선택된 영역의 좌표와 케릭터 위치, 이전 위치, 탐지 상태를 저장합니다.
capture_area = None
character_position = None
prev_position = None
detecting = False  # 탐지 상태를 나타내는 플래그

# 마우스 이벤트를 처리하는 함수
def on_click(event):
    global capture_area, selection_window

    if capture_area is None:
        capture_area = [event.x_root, event.y_root, 0, 0]
    else:
        x1, y1 = capture_area[0], capture_area[1]
        x2, y2 = event.x_root, event.y_root
        capture_area = [min(x1, x2), min(y1, y2), max(x2, x1), max(y1, y2)]
        print(f"Selected area: {capture_area}")
        selection_window.destroy()

# "영역 선택" 버튼 클릭 시 실행되는 함수
def select_area():
    global selection_window, capture_area
    capture_area = None

    selection_window = tk.Toplevel()
    selection_window.attributes('-alpha', 0.3)  # 투명도 설정
    selection_window.attributes('-fullscreen', True)  # 전체 화면 모드
    selection_window.bind('<Button-1>', on_click)  # 마우스 이벤트를 바인딩합니다.

# 케릭터 위치 선택
def on_character_click(event):
    global character_position, selection_window

    character_position = (event.x_root, event.y_root)
    selection_window.destroy()
    print(f"Character position: {character_position}")

def select_character():
    global selection_window, character_position
    character_position = None

    selection_window = tk.Toplevel()
    selection_window.attributes('-alpha', 0.3)
    selection_window.attributes('-fullscreen', True)
    selection_window.bind('<Button-1>', on_character_click)

# 이미지 크기 조정 함수
def resize_image_to_canvas(image, canvas_width, canvas_height):
    # 원본 이미지의 너비와 높이
    original_width, original_height = image.size

    # 캔버스와 이미지의 비율 계산
    ratio = min(canvas_width / original_width, canvas_height / original_height)

    # 새로운 크기 계산
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # 이미지 크기 조정
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

# 객체 탐지 함수를 주기적으로 호출하기 위한 함수
def periodic_detection():
    global capture_area, canvas, root, character_position, prev_position, detecting
    if detecting and capture_area:
        # 탐지된 이미지를 받아옴
        screenshot, prev_position = detection.detect_and_process(capture_area, character_position, prev_position)

        # 캔버스 크기에 맞게 이미지 축소
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
        resized_screenshot = resize_image_to_canvas(screenshot, canvas_width, canvas_height)

        # Tkinter와 호환되는 이미지 포맷으로 변환
        tk_image = ImageTk.PhotoImage(resized_screenshot)

        # 캔버스에 이미지 표시
        canvas.delete("all")
        canvas.create_image(0, 0, anchor='nw', image=tk_image)
        canvas.image = tk_image  # 이미지 참조 유지

        # 다음 탐지를 위해 함수 재호출
        root.after(100, periodic_detection)

# "시작" 버튼 클릭 시 실행되는 함수
def start_button_click():
    global detecting
    detecting = True
    print("Starting object detection...")
    periodic_detection()  # 주기적 탐지 시작

# "일시정지" 버튼 클릭 시 실행되는 함수
def pause_button_click():
    global detecting
    detecting = False
    print("Pausing object detection...")

# 메인 GUI 창
def main_gui():
    global root, canvas
    root = tk.Tk()
    root.title("Object Detection GUI")

    # 캔버스 생성
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()

    # "영역 선택" 버튼
    select_button = tk.Button(root, text="영역 선택", command=select_area)
    select_button.pack(side=tk.LEFT, padx=10, pady=10)

    # "케릭터" 버튼
    character_button = tk.Button(root, text="케릭터", command=select_character)
    character_button.pack(side=tk.LEFT, padx=10, pady=10)

    # "시작" 버튼
    start_button = tk.Button(root, text="시작", command=start_button_click)
    start_button.pack(side=tk.LEFT, padx=10, pady=10)

    # "일시정지" 버튼
    pause_button = tk.Button(root, text="일시정지", command=pause_button_click)
    pause_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
