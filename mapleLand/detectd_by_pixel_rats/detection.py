from PIL import ImageGrab

# 감지할 색상 설정
rgb_label_dict = {
    (0, 68, 221): "me",  # 케릭터
    (222, 85, 156): "mouse",  # 케릭터
    (231, 81, 156): "mouse",  # 케릭터
    (214, 81, 156): "mouse",  # 케릭터
    (85, 0, 33): "mouse",  # 케릭터
}


def find_color_positions(screenshot):
    """ 스크린샷에서 특정 색상의 위치를 찾는 함수 """
    pixels = screenshot.load()
    width, height = screenshot.size
    positions = {}

    for x in range(width):
        for y in range(height):
            current_color = pixels[x, y]
            if current_color in rgb_label_dict:
                label = rgb_label_dict[current_color]
                # Check if the color is (255, 255, 0) and coordinates are within 300x300 bounds
                if current_color == (255, 255, 0) and (x > 280 or y > 280):
                    continue  # Skip adding this position if outside the bounds

                if label in positions:
                    positions[label].append((x, y))
                else:
                    positions[label] = [(x, y)]
    return positions


def detect_colors(selected_area):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)
    positions = find_color_positions(screenshot)

    return screenshot, positions
