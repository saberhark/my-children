import tkinter as tk
from PIL import ImageTk, Image
import threading
import time
import detection_logic as dl  # 별도 파일로 분리된 탐지 로직

# 캔버스와 로그 영역의 크기 설정
canvas_width = 800
canvas_height = 600
log_height = 100

# 사용자가 선택한 영역과 탐지 상태 플래그
selected_area = None
detecting = False

# 기준점
reference_point = None
reference_point2 = None


def set_reference_point():
    global reference_point

    # 투명한 창을 생성하여 전체 화면을 덮습니다.
    top = tk.Toplevel(root)
    top.attributes('-fullscreen', True)
    top.attributes('-alpha', 0.3)  # 투명도 설정

    def on_fullscreen_click(event):
        global reference_point
        # 클릭된 위치를 기준점으로 설정합니다.
        reference_point = (event.x_root, event.y_root)
        print(f"Reference point set at: {reference_point}")
        top.destroy()  # 기준점 설정 후 창을 닫습니다.

    top.bind('<Button-1>', on_fullscreen_click)


def set_reference_point2():
    global reference_point2

    # 투명한 창을 생성하여 전체 화면을 덮습니다.
    top = tk.Toplevel(root)
    top.attributes('-fullscreen', True)
    top.attributes('-alpha', 0.3)  # 투명도 설정

    def on_fullscreen_click(event):
        global reference_point2
        # 클릭된 위치를 기준점으로 설정합니다.
        reference_point2 = (event.x_root, event.y_root)
        print(f"Reference point set at: {reference_point2}")
        top.destroy()  # 기준점 설정 후 창을 닫습니다.

    top.bind('<Button-1>', on_fullscreen_click)


def select_area():
    """ 사용자가 화면의 특정 영역을 선택할 수 있도록 하는 함수 """
    top = tk.Toplevel(root)
    top.attributes('-fullscreen', True)
    top.attributes('-alpha', 0.3)  # 투명도 설정
    top.bind('<Button-1>', lambda e: on_click(e, top))

    points = []

    def on_click(event, window):
        points.append((event.x_root, event.y_root))
        if len(points) == 2:
            window.destroy()
            global selected_area
            selected_area = (points[0][0], points[0][1], points[1][0], points[1][1])
            print(f"Selected area: {selected_area}")


def start_detection():
    """ 색상 탐지를 시작하는 함수 """
    global detecting
    detecting = True


def pause_detection():
    """ 색상 탐지를 일시 정지하는 함수 """
    global detecting
    detecting = False


def update_image():
    global reference_point

    """ 화면을 주기적으로 캡처하고 색상을 감지하는 함수 """
    while True:
        if selected_area and detecting:
            screenshot, pos = dl.detect_colors(selected_area, reference_point, reference_point2)
            screenshot = screenshot.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            update_canvas(screenshot)
            log_positions(pos)


def update_canvas(image):
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image


def log_positions(pos):
    #for color, pos in positions:
    log_text.insert(tk.END, f"detected at {pos}\n")
    log_text.see(tk.END)  # 로그 텍스트 박스의 스크롤을 가장 아래로 이동


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
select_area_button = tk.Button(log_frame, text="화면 지정", command=select_area)
start_button = tk.Button(log_frame, text="시작", command=start_detection)
pause_button = tk.Button(log_frame, text="일시정지", command=pause_detection)
reference_button = tk.Button(log_frame, text="기준점1(수평)", command=set_reference_point)
reference_button2 = tk.Button(log_frame, text="기준점2(수직)", command=set_reference_point2)


select_area_button.pack(side=tk.LEFT)
start_button.pack(side=tk.LEFT)
pause_button.pack(side=tk.LEFT)
reference_button.pack(side=tk.LEFT)
reference_button2.pack(side=tk.LEFT)

# 스크린샷 및 업데이트 스레드 시작
thread = threading.Thread(target=update_image, daemon=True)
thread.start()

root.mainloop()