from PIL import ImageGrab

# 감지할 색상 설정
rgb_label_dict = {
    (222, 239, 206): "zombie",    # 좀비
    (222, 235, 198): "zombie",    # 좀비
    (151, 154, 118): "zombie",    # 좀비
    (137, 120, 101): "zombie",    # 좀비
    (255, 51, 17): "zombie",    # 좀비
    (255, 255, 0): "mini_map_me",  # 케릭터 (미니맵)
    (187, 204, 68): "me",  # 케릭터
}


def find_color_positions(screenshot):
    """ 스크린샷에서 특정 색상의 위치를 찾는 함수 """
    pixels = screenshot.load()
    width, height = screenshot.size
    positions = {}

    for x in range(width):
        for y in range(height):
            if rgb_label_dict.get(pixels[x, y]):
                if positions.get(rgb_label_dict[pixels[x, y]]):
                    positions[rgb_label_dict[pixels[x, y]]].append((x, y))
                else:
                    positions[rgb_label_dict[pixels[x, y]]] = [(x, y)]
    return positions


def detect_colors(selected_area):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)
    positions = find_color_positions(screenshot)

    return screenshot, positions
