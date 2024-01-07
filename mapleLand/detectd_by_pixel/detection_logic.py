from PIL import ImageGrab, ImageDraw
import time

# 감지할 색상 설정
target_colors = {
    (99, 174, 99): "red",    # 커즈
    (187, 204, 68): "blue",  # 케릭터
    (90, 101, 115): "black",  # 케릭터 (피격)
    (71, 76, 99): "gray",   # 좀루
    (90, 105, 123): "gray",   # 좀루 (이동)
    (90, 105, 123): "gray"   # 좀루 (피격)
}


# 감지된 픽셀들
pixels = {}


def find_color_positions(screenshot):
    """ 스크린샷에서 특정 색상의 위치를 찾는 함수 """
    pixels = screenshot.load()
    width, height = screenshot.size
    positions = []

    for x in range(width):
        for y in range(height):
            if target_colors.get(pixels[x, y]):
                positions.append(((x, y), target_colors[pixels[x, y]]))
    return positions


def detect_colors(selected_area, reference_point, reference_point2):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)
    draw = ImageDraw.Draw(screenshot)

    character_pos = None
    lupin_pos = None
    curs_pos = None


    positions = find_color_positions(screenshot)
    for pos, fill_color in positions:
        left_up = (pos[0] - 25, pos[1] - 25)
        right_down = (pos[0] + 25, pos[1] + 25)
        draw.rectangle([left_up, right_down], fill=fill_color, outline=fill_color)

        if fill_color == "blue":
            character_pos = pos

    if reference_point:
        # 스크린샷 내에서의 reference_point의 y-좌표를 계산
        line_y = reference_point[1] - selected_area[1]
        draw.line((0, line_y, screenshot.width, line_y), fill="black", width=2)

    if reference_point2:
        # 스크린샷 내에서의 reference_point의 y-좌표를 계산
        line_x = reference_point2[0] - selected_area[0]
        draw.line((line_x, 0, line_x, screenshot.height), fill="black", width=2)

    return screenshot, character_pos
