import os
from PIL import Image

def convert_to_yolo_format(box, img_width, img_height):
    x_min, y_min, x_max, y_max = box
    dw = 1. / img_width
    dh = 1. / img_height
    x_center = (x_min + x_max) / 2.0 * dw
    y_center = (y_min + y_max) / 2.0 * dh
    width = (x_max - x_min) * dw
    height = (y_max - y_min) * dh
    return (x_center, y_center, width, height)

def process_annotations(annotations_data):
    output_dir = 'data/gemini_annotations'
    class_map = {"car": 0, "electric vehicle": 0, "obstacle": 1, "ev charging station": 2, "ev-charger": 2, "bollard": 1}
    os.makedirs(output_dir, exist_ok=True)

    for image_filename, annotations in annotations_data.items():
        image_path = os.path.join('data/raw/ev_charging', image_filename)
        output_filename = os.path.splitext(image_filename)[0] + '.txt'

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}. Skipping.")
            continue

        # Get image dimensions
        with Image.open(image_path) as img:
            img_width, img_height = img.size

        yolo_annotations = []
        for ann in annotations:
            class_id = class_map[ann['class_name']]
            bbox = ann['bbox']
            yolo_box = convert_to_yolo_format(bbox, img_width, img_height)
            yolo_annotations.append(f"{class_id} {' '.join(map(str, yolo_box))}")

        # Write to file
        with open(os.path.join(output_dir, output_filename), 'w') as f:
            f.write('\n'.join(yolo_annotations))

        print(f"Annotations for {image_filename} saved to {os.path.join(output_dir, output_filename)}")

if __name__ == '__main__':
    # Data for all images to be processed
    all_annotations = {
        '000149.jpg': [
            {"class_name": "car", "bbox": [0, 1030, 2460, 2720]},
            {"class_name": "ev-charger", "bbox": [1420, 280, 2030, 1710]},
            {"class_name": "ev-charger", "bbox": [1980, 150, 2690, 1750]},
            {"class_name": "ev-charger", "bbox": [2630, 115, 3340, 1760]},
            {"class_name": "ev-charger", "bbox": [3280, 160, 3930, 1790]}
        ],
        '000277.jpg': [
            {"class_name": "car", "bbox": [0, 485, 930, 2667]},
            {"class_name": "ev-charger", "bbox": [1085, 0, 3000, 2667]}
        ],
        '000175.jpg': [
            {"class_name": "car", "bbox": [1800, 1250, 4032, 3024]},
            {"class_name": "ev-charger", "bbox": [0, 250, 950, 2550]},
            {"class_name": "ev-charger", "bbox": [1000, 300, 1800, 1400]}
        ],
        '000012.jpg': [
            {"class_name": "ev-charger", "bbox": [300, 390, 1200, 1600]},
            {"class_name": "ev-charger", "bbox": [1500, 360, 2400, 1550]},
            {"class_name": "ev-charger", "bbox": [1250, 480, 1550, 900]},
            {"class_name": "ev-charger", "bbox": [1600, 490, 1900, 880]}
        ],
        '000010.png': [
            {"class_name": "ev-charger", "bbox": [200, 400, 1150, 1716]},
            {"class_name": "ev-charger", "bbox": [1600, 400, 2550, 1716]},
            {"class_name": "ev-charger", "bbox": [3100, 400, 4050, 1716]}
        ],
        '000022.jpg': [
            {"class_name": "ev-charger", "bbox": [453, 246, 804, 1005]},
            {"class_name": "ev-charger", "bbox": [297, 198, 523, 712]},
            {"class_name": "ev-charger", "bbox": [0, 348, 357, 1000]}
        ],
        '000357.jpg': [
            {"class_name": "ev-charger", "bbox": [182, 237, 957, 756]}
        ],
        '000160.jpg': [
            {"class_name": "car", "bbox": [0, 545, 808, 1080]},
            {"class_name": "ev-charger", "bbox": [763, 401, 1206, 1080]}
        ],
        '000062.jpg': [
            {"class_name": "ev-charger", "bbox": [0, 0, 608, 1080]},
            {"class_name": "car", "bbox": [748, 602, 1080, 1004]},
            {"class_name": "bollard", "bbox": [599, 550, 683, 856]},
            {"class_name": "bollard", "bbox": [678, 574, 725, 703]},
            {"class_name": "bollard", "bbox": [719, 587, 755, 654]}
        ],
        '000144.jpg': [
            {"class_name": "ev-charger", "bbox": [198, 513, 621, 905]},
            {"class_name": "ev-charger", "bbox": [1187, 511, 1605, 908]},
            {"class_name": "bollard", "bbox": [146, 750, 227, 959]},
            {"class_name": "bollard", "bbox": [700, 755, 803, 960]}
        ],
        '000235.jpg': [
            {"class_name": "car", "bbox": [453, 497, 1080, 1000]},
            {"class_name": "ev-charger", "bbox": [0, 354, 406, 911]}
        ],
        '000257.jpg': [
            {"class_name": "car", "bbox": [0, 0, 1080, 1080]}
        ],
        '000251.jpg': [
            {"class_name": "car", "bbox": [0, 0, 1080, 1080]}
        ],
        '000491.png': [
            {"class_name": "car", "bbox": [0, 304, 796, 1000]},
            {"class_name": "ev-charger", "bbox": [504, 0, 1080, 1000]}
        ]
    }
    process_annotations(all_annotations)
