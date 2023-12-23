import os
import random
import cv2
from PIL import Image, ImageOps
from sklearn.model_selection import train_test_split
import shutil

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


# 이미지 증강
def augment_and_save(image_path, label_path, output_image_folder, output_label_folder, is_mirror, is_noisy):
    # 이미지 불러오기 및 그레이스케일 변환
    image = Image.open(image_path).convert('L')
    label_data = open(label_path, 'r').readlines()
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    suffix = ''

    # 이미지 좌우 대칭
    if is_mirror:
        suffix += '_mirror'
        image = ImageOps.mirror(image)
        label_data = mirror_label(label_data)

    # 잘림 및 가림 적용
    if is_noisy:
        suffix += '_noisy'
        image, label_data = crop_and_cover(image, label_data)

    # 이미지 및 라벨 저장
    # 변경된 이미지 및 라벨 저장
    output_image_filename = f"{base_filename}{suffix}.jpg"
    output_label_filename = f"{base_filename}{suffix}.txt"
    output_image_path = os.path.join(output_image_folder, output_image_filename)
    output_label_path = os.path.join(output_label_folder, output_label_filename)

    image.save(output_image_path)
    with open(output_label_path, 'w') as f:
        f.writelines(label_data)


def mirror_label(label_data):
    # YOLO 라벨 좌우 대칭 변환
    mirrored_labels = []
    for line in label_data:
        parts = line.strip().split()
        x_center = 1 - float(parts[1])  # x_center 좌우 대칭
        mirrored_labels.append(f"{parts[0]} {x_center} {parts[2]} {parts[3]} {parts[4]}\n")
    return mirrored_labels


def adjust_labels_for_crop_and_cover(labels, crop_x, crop_y, w, h, is_crop, is_cover):
    adjusted_labels = []
    for label in labels:
        parts = label.strip().split()
        class_id, x_center, y_center, width, height = map(float, parts)

        # YOLO 형식의 라벨을 이미지 좌표로 변환
        x_min = (x_center - width / 2) * w
        y_min = (y_center - height / 2) * h
        x_max = (x_center + width / 2) * w
        y_max = (y_center + height / 2) * h

        if is_crop:
            # 이미지가 잘릴 경우 라벨 조정
            x_min = max(x_min - crop_x, 0)
            y_min = max(y_min - crop_y, 0)
            x_max = min(x_max - crop_x, w - 2 * crop_x)
            y_max = min(y_max - crop_y, h - 2 * crop_y)
            new_w, new_h = w - 2 * crop_x, h - 2 * crop_y
        elif is_cover:
            # 이미지에 가림이 적용될 경우 라벨 조정
            cover_x, cover_y = random.randint(0, w - crop_x), random.randint(0, h - crop_y)
            if cover_x < x_min < cover_x + crop_x or cover_x < x_max < cover_x + crop_x:
                x_min, x_max = max(x_min, cover_x + crop_x), min(x_max, cover_x)
            if cover_y < y_min < cover_y + crop_y or cover_y < y_max < cover_y + crop_y:
                y_min, y_max = max(y_min, cover_y + crop_y), min(y_max, cover_y)
            new_w, new_h = w, h

        # 조정된 좌표를 다시 YOLO 형식으로 변환
        x_center = ((x_min + x_max) / 2) / new_w
        y_center = ((y_min + y_max) / 2) / new_h
        width = (x_max - x_min) / new_w
        height = (y_max - y_min) / new_h

        # 조정된 라벨이 유효한 경우에만 추가
        if 0 < x_center < 1 and 0 < y_center < 1 and width > 0 and height > 0:
            adjusted_labels.append(f"{class_id} {x_center} {y_center} {width} {height}\n")

    return adjusted_labels


def crop_and_cover(image, label_data):
    w, h = image.size
    crop_x = random.randint(0, w // 4)
    crop_y = random.randint(0, h // 4)
    is_crop = random.random() > 0.5
    is_cover = not is_crop

    if is_crop:
        # 이미지 잘림 적용
        image = image.crop((crop_x, crop_y, w - crop_x, h - crop_y))
    else:
        # 이미지 가림 적용
        cover = Image.new('L', (crop_x, crop_y), 'black')
        cover_x, cover_y = random.randint(0, w - crop_x), random.randint(0, h - crop_y)
        image.paste(cover, (cover_x, cover_y))

    adjusted_labels = adjust_labels_for_crop_and_cover(label_data, crop_x, crop_y, w, h, is_crop, is_cover)
    return image, adjusted_labels


if __name__ == '__main__':
    train_dir = 'train'
    output_image_folder = 'pretreated_/images'
    output_label_folder = 'pretreated/labels'

    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    # 모든 이미지에 대해 그레이스케일, 좌우 대칭 및 노이즈 적용
    for filename in os.listdir(train_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(train_dir, filename)
            label_path = image_path.replace('.jpg', '.txt')

            # 그레이스케일 저장
            augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, False)

            # 좌우 대칭 저장
            augment_and_save(image_path, label_path, output_image_folder, output_label_folder, True, False)

            # 선택적으로 노이즈 적용
            if random.random() > 0.5:
                augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, True)

    # 8:2 비율로 train, val 분리
    images = [f for f in os.listdir(output_image_folder) if f.endswith('.jpg')]
    labels = [f.replace('.jpg', '.txt') for f in images]
    train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2)

    # 훈련 및 검증 데이터셋 폴더 생성
    train_image_folder = 'new_dataset/images/train'
    val_image_folder = 'new_dataset/images/val'
    os.makedirs(train_image_folder, exist_ok=True)
    os.makedirs(val_image_folder, exist_ok=True)

    # 훈련 데이터셋 이동
    for img, lbl in zip(train_images, train_labels):
        shutil.move(os.path.join(output_image_folder, img), train_image_folder)
        shutil.move(os.path.join(output_label_folder, lbl), train_image_folder)

    # 검증 데이터셋 이동
    for img, lbl in zip(val_images, val_labels):
        shutil.move(os.path.join(output_image_folder, img), val_image_folder)
        shutil.move(os.path.join(output_label_folder, lbl), val_image_folder)

    print("Dataset separation and moving completed.")
