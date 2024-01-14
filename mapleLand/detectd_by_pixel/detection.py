from PIL import ImageGrab, ImageDraw
import math

# 감지할 색상 설정
target_colors = {
    (99, 174, 99): "red",    # 커즈
    (187, 204, 68): "blue",  # 케릭터
    (60, 51, 0): "blue",  # 케릭터 (피격)
    (71, 76, 99): "gray",   # 좀루
    (90, 105, 123): "gray",   # 좀루 (이동)
    (90, 101, 115): "gray"   # 좀루 (피격)
}


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


def calculate_distance(pos1, pos2):
    """ Calculate the distance between two points """
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def find_closest_positions(character_pos, positions):
    """ Find the closest gray and red positions to the character """
    closest_gray = None
    closest_red = None
    min_gray_distance = float('inf')
    min_red_distance = float('inf')

    for pos, color in positions:
        distance = calculate_distance(character_pos, pos)
        if color == 'gray' and distance < min_gray_distance:
            closest_gray = pos
            min_gray_distance = distance
        elif color == 'red' and distance < min_red_distance:
            closest_red = pos
            min_red_distance = distance

    return closest_gray, closest_red


def draw_detected_areas(draw, positions):
    """ 감지된 영역에 사각형을 그리는 함수 """
    for pos, fill_color in positions:
        left_up = (pos[0] - 25, pos[1] - 25)
        right_down = (pos[0] + 25, pos[1] + 25)
        draw.rectangle([left_up, right_down], fill=fill_color, outline=fill_color)


def draw_reference_lines(draw, screenshot, reference_point, reference_point2, selected_area):
    """ 참조선을 그리는 함수 """
    if reference_point:
        line_y = reference_point[1] - selected_area[1]
        draw.line((0, line_y, screenshot.width, line_y), fill="black", width=2)
    if reference_point2:
        line_x = reference_point2[0] - selected_area[0]
        draw.line((line_x, 0, line_x, screenshot.height), fill="black", width=2)


def detect_colors(selected_area, reference_point, reference_point2):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)
    draw = ImageDraw.Draw(screenshot)

    positions = find_color_positions(screenshot)
    draw_detected_areas(draw, positions)

    character_pos = next((pos for pos, color in positions if color == "blue"), None)

    closest_gray, closest_red = None, None

    if character_pos:
        closest_gray, closest_red = find_closest_positions(character_pos, positions)

    draw_reference_lines(draw, screenshot, reference_point, reference_point2, selected_area)

    return screenshot, character_pos, closest_gray, closest_red
