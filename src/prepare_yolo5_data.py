import os
import shutil
from sklearn.model_selection import train_test_split

def prepare_data():
    # Directories
    image_source_dir = 'data/raw'
    primary_label_source_dir = 'data/gemini_annotations'
    secondary_label_source_dir = 'data/yolo_annotations'

    train_img_dir = 'data/images/train'
    val_img_dir = 'data/images/val'
    train_label_dir = 'data/labels/train'
    val_label_dir = 'data/labels/val'

    # Create directories if they don't exist
    for path in [train_img_dir, val_img_dir, train_label_dir, val_label_dir]:
        os.makedirs(path, exist_ok=True)

    # Get all image files recursively
    image_paths = []
    for root, _, files in os.walk(image_source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))

    # Filter for images that have corresponding annotations
    valid_image_paths = []
    for img_path in image_paths:
        img_file = os.path.basename(img_path)
        label_filename = os.path.splitext(img_file)[0] + '.txt'
        primary_label_path = os.path.join(primary_label_source_dir, label_filename)
        secondary_label_path = os.path.join(secondary_label_source_dir, label_filename)

        if os.path.exists(primary_label_path) or os.path.exists(secondary_label_path):
            valid_image_paths.append(img_path)

    print(f"Found {len(valid_image_paths)} images with corresponding annotations.")

    # Split data
    train_files, val_files = train_test_split(valid_image_paths, test_size=0.2, random_state=42)

    # Function to copy files
    def copy_files(files, img_dest, label_dest):
        for file_path in files:
            file_name = os.path.basename(file_path)
            # Copy image
            shutil.copy(file_path, os.path.join(img_dest, file_name))
            # Copy label
            label_filename = os.path.splitext(file_name)[0] + '.txt'
            primary_label_path = os.path.join(primary_label_source_dir, label_filename)
            secondary_label_path = os.path.join(secondary_label_source_dir, label_filename)

            if os.path.exists(primary_label_path):
                shutil.copy(primary_label_path, os.path.join(label_dest, label_filename))
            elif os.path.exists(secondary_label_path):
                shutil.copy(secondary_label_path, os.path.join(label_dest, label_filename))

    # Copy files to new directories
    print(f"Copying {len(train_files)} files to training set...")
    copy_files(train_files, train_img_dir, train_label_dir)
    print(f"Copying {len(val_files)} files to validation set...")
    copy_files(val_files, val_img_dir, val_label_dir)

    print("Data preparation complete.")

if __name__ == '__main__':
    prepare_data()
