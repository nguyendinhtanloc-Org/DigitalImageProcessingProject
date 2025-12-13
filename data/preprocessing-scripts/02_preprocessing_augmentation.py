import os
import cv2
import numpy as np
import shutil
import random

from utils import (
    apply_clahe,
    apply_homomorphic_filter,
    resize_with_padding
)

INPUT_DATA_DIR = "./data/interim"
PROCESSED_DATA_DIR = "./data/processed_final"
SEED = 42

random.seed(SEED)
np.random.seed(SEED)


def do_rotate(image):
    rows, cols = image.shape[:2]
    angle = random.uniform(-5, 5)
    matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    return cv2.warpAffine(image, matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT)


def do_zoom(image):
    factor = random.uniform(1.0, 1.1)
    h, w = image.shape[:2]
    new_h, new_w = int(h / factor), int(w / factor)
    top = (h - new_h) // 2
    left = (w - new_w) // 2
    cropped = image[top:top + new_h, left:left + new_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)


def do_shift(image):
    rows, cols = image.shape[:2]
    tx = random.uniform(-0.05, 0.05) * cols
    ty = random.uniform(-0.05, 0.05) * rows
    matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT)


def do_blur(image):
    return cv2.GaussianBlur(image, (3, 3), 0)


def do_sharpen(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


TRANSFORMS = [
    (do_rotate, "rot"),
    (do_zoom, "zoom"),
    (do_shift, "shift"),
    (do_blur, "blur"),
    (do_sharpen, "sharp")
]


def full_pipeline_process(image, is_augmentation=False, transform_func=None):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if is_augmentation and transform_func is not None:
        image = transform_func(image)

    image = resize_with_padding(image, target_size=256)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = apply_homomorphic_filter(image, d0=30, gamma_l=0.5, gamma_h=1.2)
    image = apply_clahe(image)
    return image


def process_split_category(split, category):
    src_path = os.path.join(INPUT_DATA_DIR, split, category)
    dst_path = os.path.join(PROCESSED_DATA_DIR, split, category)

    if not os.path.exists(src_path):
        return

    files = os.listdir(src_path)
    print(f"Đang xử lý: {split}/{category} ({len(files)} ảnh)")

    for file_name in files:
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            src_file = os.path.join(src_path, file_name)
            image = cv2.imread(src_file)
            if image is None:
                continue

            clean = full_pipeline_process(image, is_augmentation=False)
            cv2.imwrite(os.path.join(dst_path, file_name), clean)

            if split == "train":
                base, ext = os.path.splitext(file_name)

                if category == "NORMAL":
                    chosen_transforms = TRANSFORMS
                else:
                    chosen_transforms = [t for t in TRANSFORMS if t[1] in ("rot", "shift")]

                for func, suffix in chosen_transforms:
                    aug = full_pipeline_process(image, is_augmentation=True, transform_func=func)
                    new_name = f"{base}_{suffix}{ext}"
                    cv2.imwrite(os.path.join(dst_path, new_name), aug)

        except Exception as error:
            print(f"Lỗi file {file_name}: {error}")


def main():
    if os.path.exists(PROCESSED_DATA_DIR):
        shutil.rmtree(PROCESSED_DATA_DIR)

    for split in ["train", "val", "test"]:
        for category in ["NORMAL", "PNEUMONIA"]:
            os.makedirs(os.path.join(PROCESSED_DATA_DIR, split, category), exist_ok=True)

    print(f"Bắt đầu xử lý dữ liệu từ {INPUT_DATA_DIR}")
    print("Phương án: Offline Augmentation")

    for split in ["train", "val", "test"]:
        for category in ["NORMAL", "PNEUMONIA"]:
            process_split_category(split, category)

    print("Hoàn tất")
    print(f"Dữ liệu cuối cùng tại: {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    main()
