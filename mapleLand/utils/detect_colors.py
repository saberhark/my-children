import winsound
from PIL import ImageGrab

from mapleLand.utils.alert import alert
from mapleLand.utils.colors import rgb_label_dict as default_rgb_label_dict


def detect_colors(selected_area, rgb_label_dict=default_rgb_label_dict):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)

    """ 스크린샷에서 특정 색상의 위치를 찾는 함수 """
    pixels = screenshot.load()
    width, height = screenshot.size
    positions = {}
    alert_triggered = False

    for x in range(width):
        for y in range(height):
            current_color = pixels[x, y]
            if current_color in rgb_label_dict:
                label = rgb_label_dict[current_color]
                # Check if the color is (255, 255, 0) and coordinates are within 300x300 bounds
                #if label == 'mini_map_me' and ((x > 280 or y > 150) or 'mini_map_me' in positions):
                if label == 'mini_map_me' and ((x > 320 or y > 270) or 'mini_map_me' in positions):
                    continue  # Skip adding this position if outside the bounds

                if label == 'alert':
                    #if x < 280 and y < 150 and not alert_triggered:
                    if x < 320 and y < 270 and not alert_triggered:
                        alert()
                        alert_triggered = True
                    continue  # Skip adding this position if outside the bounds

                if label in positions:
                    positions[label].append((x, y))
                else:
                    positions[label] = [(x, y)]

    return screenshot, positions
