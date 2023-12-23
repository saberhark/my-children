import os
import shutil
import cv2
from sklearn.model_selection import train_test_split
from PIL import Image, ImageOps
import random
import os

# 라벨별 데이터 갯수 파악
def data_count():
    label_dict = {}
    # 'dataset/labels/train' 폴더의 모든 파일을 순회
    for filename in os.listdir('train'):
        if filename.endswith('.txt'):
            with open(f'train/{filename}', 'r') as file:
                labels = file.readlines()
                for label_line in labels:
                    # 라인에서 첫 번째 공백 전까지의 문자열을 추출하여 라벨로 사용
                    label = int(label_line.split()[0])
                    # 해당 라벨의 발견 횟수를 label_dict에 저장하고, 이미 존재하는 경우 값을 1 증가
                    label_dict[label] = label_dict.get(label, 0) + 1

    # label_dict를 출력
    print("Label Dictionary:")
    for label, count in label_dict.items():
        print(f'{label}: {count}')

def separate_train_val():
    # 이미지 파일 경로와 라벨 파일 경로를 저장할 리스트
    image_paths = []
    label_paths = []

    # 이미지 파일과 라벨을 로드하는 코드
    for filename in os.listdir('train'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join('train', filename)
            label_path = os.path.join('train', os.path.splitext(filename)[0] + '.txt')

            image_paths.append(image_path)
            label_paths.append(label_path)

    # 훈련 데이터와 검증 데이터로 분할 (8:2 비율)
    train_image_paths, val_image_paths, train_label_paths, val_label_paths = train_test_split(
        image_paths, label_paths, test_size=0.2
    )
    return train_image_paths, val_image_paths, train_label_paths, val_label_paths

def copy_files(file_paths, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for path in file_paths:
        shutil.copy(path, output_folder)

# 이미지를 그레이스케일로 변환하고 저장하는 함수
def convert_to_grayscale_and_save(image_paths, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for path in image_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        output_path = os.path.join(output_folder, os.path.basename(path))
        cv2.imwrite(output_path, img)

# 훈련 데이터와 검증 데이터를 분할하고 복사
train_image_paths, val_image_paths, train_label_paths, val_label_paths = separate_train_val()
convert_to_grayscale_and_save(train_image_paths, r'./dataset/train_grayscale')
convert_to_grayscale_and_save(val_image_paths, r'./dataset/val_grayscale')
copy_files(train_label_paths, r'./dataset/train_labels')
copy_files(val_label_paths, r'./dataset/val_labels')



def augment_image(image_path, output_path, augment_count=5):
    """ 이미지를 읽고, 증강 후 저장 """
    image = Image.open(image_path).convert('L')  # 그레이스케일로 변환
    for i in range(augment_count):
        augmented_image = image.copy()

        # 좌우 반전
        if random.random() > 0.5:
            augmented_image = ImageOps.mirror(augmented_image)

        # 절단 및 가림
        augmented_image = crop_and_cover(augmented_image)

        augmented_image.save(os.path.join(output_path, f"{i}_{os.path.basename(image_path)}"))

def crop_and_cover(image):
    """ 이미지의 일부를 절단하거나 가림 """
    w, h = image.size
    crop_x = random.randint(0, w // 4)
    crop_y = random.randint(0, h // 4)

    # 이미지 절단
    if random.random() > 0.5:
        image = image.crop((crop_x, crop_y, w - crop_x, h - crop_y))

    # 이미지 가림
    else:
        cover = Image.new('L', (crop_x, crop_y), 'black')
        image.paste(cover, (random.randint(0, w - crop_x), random.randint(0, h - crop_y)))

    return image

# 증강할 이미지의 경로
image_path = 'path/to/your/image.jpg'

# 증강된 이미지를 저장할 경로
output_path = 'path/to/augmented/images'

# 이미지 증강 실행
augment_image(image_path, output_path, augment_count=5)
