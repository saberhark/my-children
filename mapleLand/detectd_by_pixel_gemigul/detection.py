from PIL import ImageGrab

# 감지할 색상 설정
rgb_label_dict = {
    (66, 106, 121): "horn",
    (255, 255, 0): "mini_map_me",  # 케릭터 (미니맵)
    (222, 205, 192): "horn",  # 케릭터 (미니맵)
    (173, 154, 140): "horn",  # 케릭터 (미니맵)
    (0, 68, 221): "me",  # 케릭터
}