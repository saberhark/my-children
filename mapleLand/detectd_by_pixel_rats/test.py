import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import threading
import time

from mapleLand.detectd_by_pixel_gemigul.detection import find_color_positions


def update_image(canvas, bbox):
    while True:
        screenshot = ImageGrab.grab(bbox=bbox)
        positions = find_color_positions(screenshot)
        pixels = screenshot.load()
        for label, pos_list in positions.items():
            for x, y in pos_list:
                pixels[x, y] = (0, 255, 0)  # Red for detected positions

        photo = ImageTk.PhotoImage(screenshot)
        canvas.image = photo  # Keep a reference!
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        time.sleep(0.5)  # Update interval

def main():
    root = tk.Tk()
    bbox = (0, 0, 800, 600)  # Customize this area based on your screen dimensions

    canvas = tk.Canvas(root, width=bbox[2], height=bbox[3])
    canvas.pack()

    thread = threading.Thread(target=update_image, args=(canvas, bbox))
    thread.daemon = True
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
