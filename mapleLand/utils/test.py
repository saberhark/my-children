import tkinter as tk
from PIL import ImageTk, ImageGrab
import threading
import time
import pygetwindow as gw

from mapleLand.utils.colors import rgb_label_dict
from mapleLand.utils.detect_colors import detect_colors

def get_maplestory_window():
    """ 'MapleStory Worlds-Mapleland' 창의 위치와 크기를 반환하는 함수 """
    try:
        window = gw.getWindowsWithTitle('MapleStory Worlds-Mapleland')[0]
        if window:
            return window.left, window.top, window.width, window.height
    except IndexError:
        print("MapleStory 창을 찾을 수 없습니다.")
        return None

def update_image(canvas, label):
    while True:
        bbox = get_maplestory_window()
        if bbox:
            left, top, width, height = bbox
            bbox = (left, top, left + width, top + height)
            screenshot, positions = detect_colors(bbox, rgb_label_dict)
            pixels = screenshot.load()

            # 발견된 부분 색칠
            mini_map_me_positions = []
            for label_name, pos_list in positions.items():
                for x, y in pos_list:
                    pixels[x, y] = (0, 255, 0)  # Green for detected positions
                    if label_name == 'mini_map_me':
                        mini_map_me_positions.append((x, y))

            # Update the label text with the positions of 'mini_map_me'
            label_text = "Mini Map Me positions: " + ", ".join(f"({x}, {y})" for x, y in mini_map_me_positions)
            label.config(text=label_text)

            photo = ImageTk.PhotoImage(screenshot)
            canvas.image = photo  # Keep a reference!
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        else:
            label.config(text="MapleStory 창을 찾을 수 없습니다.")
        time.sleep(0.5)  # Update interval


def main():
    root = tk.Tk()
    root.title("Color Detection Viewer")

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # Create a label for displaying positions
    label = tk.Label(root, text="Mini Map Me positions: None", font=('Helvetica', 10))
    label.pack()

    thread = threading.Thread(target=update_image, args=(canvas, label))
    thread.daemon = True
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
