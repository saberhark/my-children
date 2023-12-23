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


def cover_object_and_adjust_labels(image, label_data, cover_ratio=0.3):
    w, h = image.size

    for label in label_data:
        parts = label.strip().split()
        class_id, x_center, y_center, width, height = map(float, parts)

        x_min = int((x_center - width / 2) * w)
        y_min = int((y_center - height / 2) * h)
        x_max = int((x_center + width / 2) * w)
        y_max = int((y_center + height / 2) * h)

        cover_width = int(width * w * cover_ratio)
        cover_height = int(height * h * cover_ratio)

        cover_y_range = int(height * h * 0.10)  # 객체 높이의 15%
        cover_y = random.randint(y_max - cover_height - cover_y_range, y_max - cover_height)
        cover_x = random.randint(x_min, x_max - cover_width)

        # 이미지에 커버 노이즈 적용
        cover = Image.new('L', (cover_width, cover_height), 'black')
        image.paste(cover, (cover_x, cover_y))

    return image, label_data  # 라벨 데이터는 변경 없이 반환




# 이미지 증강
def augment_and_save(image_path, label_path, output_image_folder, output_label_folder, is_mirror, is_noisy, ratio=0.3):
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
        suffix += '_noisy_'+ str(ratio)
        image, label_data = cover_object_and_adjust_labels(image, label_data, ratio)

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
            augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, True, 0.3)
            #augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, True, 0.3)
            #augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, True, 0.4)
            augment_and_save(image_path, label_path, output_image_folder, output_label_folder, False, True, 0.5)

    # 8:2 비율로 train, val 분리
    images = [f for f in os.listdir(output_image_folder) if f.endswith('.jpg')]
    labels = [f.replace('.jpg', '.txt') for f in images]
    train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2)

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

    print("Dataset preparation completed.")