import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import threading
import time

# 전역 변수 설정
capture_area = None
detecting = False
processed_img = None

def on_click(event, window):
    """ 마우스 클릭 이벤트 핸들러 """
    global capture_area
    if capture_area is None:
        capture_area = [event.x_root, event.y_root, 0, 0]
    else:
        capture_area[2], capture_area[3] = event.x_root, event.y_root
        print(f"Selected area: {capture_area}")
        window.destroy()

def select_area():
    global capture_area
    capture_area = None
    """ 영역 선택을 위한 창을 열고 이벤트를 바인딩 """
    selection_window = tk.Toplevel()
    selection_window.attributes('-alpha', 0.3)
    selection_window.attributes('-fullscreen', True)
    selection_window.bind('<Button-1>', lambda e: on_click(e, selection_window))

def update_image():
    """ 스크린샷을 캡처하고 이미지를 처리 """
    global capture_area, detecting, processed_img
    while True:
        if detecting and capture_area:
            # 스크린샷 캡처
            x1, y1, x2, y2 = capture_area
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            # 필요한 이미지 처리 수행
            # 예: 색상 탐지, 객체 인식 등

            processed_img = screenshot
        time.sleep(0.1)

def update_canvas():
    """ 캔버스 업데이트 """
    global processed_img, canvas
    if processed_img:
        img = ImageTk.PhotoImage(processed_img)
        canvas.create_image(0, 0, anchor='nw', image=img)
        canvas.image = img

def start_detection():
    """ 탐지 시작 """
    global detecting
    detecting = True
    print("Detection started")

def pause_detection():
    """ 탐지 일시 중지 """
    global detecting
    detecting = False
    print("Detection paused")

# 메인 GUI
root = tk.Tk()
root.title("Screen Detection")

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

select_button = tk.Button(root, text="영역 선택", command=select_area)
select_button.pack(side=tk.LEFT)

start_button = tk.Button(root, text="시작", command=start_detection)
start_button.pack(side=tk.LEFT)

pause_button = tk.Button(root, text="일시정지", command=pause_detection)
pause_button.pack(side=tk.LEFT)

# 스크린샷 및 이미지 처리 스레드 시작
thread = threading.Thread(target=update_image, daemon=True)
thread.start()

# 주기적으로 캔버스 업데이트
def periodic_canvas_update():
    update_canvas()
    root.after(100, periodic_canvas_update)

root.after(100, periodic_canvas_update)
root.mainloop()
