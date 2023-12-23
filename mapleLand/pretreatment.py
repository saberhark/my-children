import os
import random

import cv2
from PIL import Image, ImageOps
from sklearn.model_selection import train_test_split


def data_count(path):
    label_dict = {}
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            with open(os.path.join(path, filename), 'r') as file:
                labels = file.readlines()
                for label_line in labels:
                    label = int(label_line.split()[0])
                    label_dict[label] = label_dict.get(label, 0) + 1
    return label_dict

def separate_train_val(image_dir, test_size=0.2):
    image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    label_paths = [p.replace('.jpg', '.txt').replace('.png', '.txt') for p in image_paths]

    train_image_paths, val_image_paths, train_label_paths, val_label_paths = train_test_split(
        image_paths, label_paths, test_size=test_size
    )
    return train_image_paths, val_image_paths, train_label_paths, val_label_paths


def convert_to_grayscale_and_save(image_paths, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for path in image_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        output_path = os.path.join(output_folder, os.path.basename(path))
        cv2.imwrite(output_path, img)


def augment_image(image_path, output_path, augment_count=5):
    image = Image.open(image_path).convert('L')
    for i in range(augment_count):
        augmented_image = image.copy()

        if random.random() > 0.5:
            augmented_image = ImageOps.mirror(augmented_image)

        augmented_image = crop_and_cover(augmented_image)
        augmented_image.save(os.path.join(output_path, f"{i}_{os.path.basename(image_path)}"))


def crop_and_cover(image):
    w, h = image.size
    crop_x = random.randint(0, w // 4)
    crop_y = random.randint(0, h // 4)

    if random.random() > 0.5:
        image = image.crop((crop_x, crop_y, w - crop_x, h - crop_y))
    else:
        cover = Image.new('L', (crop_x, crop_y), 'black')
        image.paste(cover, (random.randint(0, w - crop_x), random.randint(0, h - crop_y)))

    return image


if __name__ == '__main__':
    # 데이터셋 디렉터리 설정
    train_dir = 'path/to/train/dataset'

    # 데이터 카운트
    label_counts = data_count(train_dir)
    print("Label counts:", label_counts)

    # 훈련 및 검증 데이터 분할
    train_images, val_images, train_labels, val_labels = separate_train_val(train_dir)

    # 이미지를 그레이스케일로 변환하고 저장
    convert_to_grayscale_and_save(train_images, './dataset/train_grayscale')
    convert_to_grayscale_and_save(val_images, './dataset/val_grayscale')

    # 증강 이미지 저장 경로 설정
    augmented_image_path = 'path/to/augmented/images'

    # 이미지 증강 실행
    for image_path in train_images:
        augment_image(image_path, augmented_image_path)