from PIL import ImageGrab

# 감지할 색상 설정
target_colors = {
    (189, 222, 222): "red",    # 레이스
    #(187, 222, 222): "red",  # 레이스
    (255, 255, 0): "gray",  # 케릭터 (미니맵)
    (102, 221, 255): "purple",  # 포탈 (미니맵)
    (187, 204, 68): "blue",  # 케릭터
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


# 범위 내의 객체가 있다면 리턴 끝
def find_wraith(positions):
    red_positions = []
    for pos, color in positions:
        if color == 'red':
            red_positions.append(pos)
    return red_positions


def detect_colors(selected_area):
    """ 지정된 영역에서 색상을 탐지하고 처리된 이미지를 반환하는 함수 """
    screenshot = ImageGrab.grab(bbox=selected_area)

    positions = find_color_positions(screenshot)

    character_pos = next((pos for pos, color in positions if color == "blue"), None)
    mini_map_me = next((pos for pos, color in positions if color == "gray"), None)
    mini_map_portal = next((pos for pos, color in positions if color == "purple"), None)
    wraiths = find_wraith(positions)

    return screenshot, character_pos, wraiths, mini_map_me, mini_map_portal
