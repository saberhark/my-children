import os
import shutil


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def move_files(src_folder, dest_image_folder, dest_label_folder):
    ensure_dir(dest_image_folder)
    ensure_dir(dest_label_folder)

    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        if filename.endswith('.jpg'):
            dest_path = os.path.join(dest_image_folder, filename)
        elif filename.endswith('.txt'):
            dest_path = os.path.join(dest_label_folder, filename)
        else:
            continue  # 파일 확장자가 .jpg나 .txt가 아닌 경우 무시
        shutil.move(src_path, dest_path)


# 훈련 데이터셋 이동
move_files('new_dataset/images/train', 'dataset/images/train', 'dataset/labels/train')

# 검증 데이터셋 이동
move_files('new_dataset/images/val', 'dataset/images/val', 'dataset/labels/val')
