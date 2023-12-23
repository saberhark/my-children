import cv2
import os

def draw_labels(image_path, label_path, output_path):
    # 이미지 로드
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    # 라벨 파일 로드 및 바운딩 박스 그리기
    with open(label_path, 'r') as file:
        for line in file.readlines():
            class_id, x_center, y_center, width, height = map(float, line.split())
            x_center, y_center, width, height = x_center * w, y_center * h, width * w, height * h
            x_min, y_min = int(x_center - width / 2), int(y_center - height / 2)
            x_max, y_max = int(x_center + width / 2), int(y_center + height / 2)
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image, str(class_id), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 변환된 이미지 저장
    cv2.imwrite(output_path, image)

# 이미지 및 라벨 경로 설정
image_dir = 'new_dataset/images/train'
output_dir = 'new_dataset/annotated_images'
os.makedirs(output_dir, exist_ok=True)

# 모든 이미지에 대해 라벨링 및 저장
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        image_path = os.path.join(image_dir, filename)
        label_path = os.path.join(image_dir, filename.replace('.jpg', '.txt'))
        output_path = os.path.join(output_dir, filename)
        draw_labels(image_path, label_path, output_path)

print("All images have been processed and saved.")
