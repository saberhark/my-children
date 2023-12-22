import os
import xml.etree.ElementTree as ET

# 주어진 클래스 이름에 대한 ID 매핑
classes = {'me': 0, 'name': 1, 'monster': 2, 'ladder': 3}
class_ids = {name: idx for idx, name in enumerate(classes)}


def convert_annotation(xml_file, output_txt_file):
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
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / 2 / img_width
    y_center = (y_min + y_max) / 2 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height


# 'annotations' 폴더 내의 모든 XML 파일을 YOLO 형식으로 변환합니다.
# 해당 디렉토리와 파일들은 실제 환경에 맞게 조정되어야 합니다.
for xml_file in os.listdir(r'./frame'):
    if xml_file.endswith('.xml'):
        output_txt_file = os.path.join(r'./frame', os.path.splitext(xml_file)[0] + '.txt')
        convert_annotation(os.path.join(r'./frame', xml_file), output_txt_file)

print("Conversion completed.")
