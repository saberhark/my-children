import os
import shutil
import xml.etree.ElementTree as ET

# 주어진 클래스 이름에 대한 ID 매핑
classes = {'me': 0, 'name': 1, 'horn_mush': 2, 'zombie_mush': 3, 'ladder': 4}
class_ids = {name: idx for idx, name in enumerate(classes)}


def convert_annotation(xml_file, output_txt_file):
    # XML 파일을 파싱
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(output_txt_file, 'w') as file:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in class_ids:
                continue
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
            img_width = int(root.find('size').find('width').text)
            img_height = int(root.find('size').find('height').text)
            bb = convert_to_yolo_format(b, img_width, img_height)

            file.write(f"{class_ids[cls]} {' '.join([str(a) for a in bb])}\n")


def convert_to_yolo_format(box, img_width, img_height):
    # 박스 정보를 YOLO 형식으로 변환
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / 2 / img_width
    y_center = (y_min + y_max) / 2 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height


# 'a' 폴더 생성 (이미 존재하지 않는 경우)
output_folder = r'./train'
os.makedirs(output_folder, exist_ok=True)


# 'zombie' 폴더 내의 모든 XML 파일을 처리
for xml_file in os.listdir(r'./zombie'):
    if xml_file.endswith('.xml'):
        base_filename = os.path.splitext(xml_file)[0]
        output_txt_file = os.path.join(output_folder, base_filename + '.txt')
        convert_annotation(os.path.join(r'./zombie', xml_file), output_txt_file)

        # 원본 이미지 파일 찾기 및 복사
        image_file = os.path.join(r'./zombie', base_filename + '.jpg')
        if os.path.exists(image_file):
            shutil.copy(image_file, output_folder)


print("Conversion and copying completed.")
