import os
import cv2
import numpy as np
import shutil
import random
from utils import apply_clahe, apply_homomorphic_filter, resize_with_padding

INPUT_DATA_DIR = "data/interim"
PROCESSED_DATA_DIR = "data/processed"
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

def do_rotate(image):
    rows, cols = image.shape[:2]
    angle = random.uniform(-5, 5) 
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT)

def do_zoom(image):
    zoom_factor = random.uniform(1.0, 1.1)
    h, w = image.shape[:2]
    new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)
    top = (h - new_h) // 2
    left = (w - new_w) // 2
    cropped = image[top:top+new_h, left:left+new_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

def do_shift(image):
    rows, cols = image.shape[:2]
    tx = random.uniform(-0.05, 0.05) * cols
    ty = random.uniform(-0.05, 0.05) * rows
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT)

def do_blur(image):
    return cv2.GaussianBlur(image, (3, 3), 0)

def do_sharpen(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

TRANSFORMS = [
    (do_rotate, "rot"), 
    (do_zoom, "zoom"),
    (do_shift, "shift"), 
    (do_blur, "blur"), 
    (do_sharpen, "sharp")
]

def full_pipeline_process(img, is_augmentation=False, transform_func=None):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    if is_augmentation and transform_func:
        img = transform_func(img)
        
    img = resize_with_padding(img, target_size=256)
    
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = apply_homomorphic_filter(img, d0=30, gamma_l=0.5, gamma_h=1.2) # Giảm gamma_h xuống 1.2 cho đỡ gai
    img = apply_clahe(img)
    
    return img

def main():
    if os.path.exists(PROCESSED_DATA_DIR):
        print(f"Đang xóa dữ liệu cũ tại {PROCESSED_DATA_DIR}...")
        shutil.rmtree(PROCESSED_DATA_DIR)

    for split in ['train', 'val', 'test']:
        for category in ['NORMAL', 'PNEUMONIA']:
            os.makedirs(os.path.join(PROCESSED_DATA_DIR, split, category), exist_ok=True)

    print(f"Bắt đầu xử lý dữ liệu từ {INPUT_DATA_DIR}...")
    print("Chiến lược: Offline Augmentation (Cân bằng Normal/Pneumonia cho tập Train)")

    splits = ['train', 'val', 'test']
    
    for split in splits:
        for category in ['NORMAL', 'PNEUMONIA']:
            src_path = os.path.join(INPUT_DATA_DIR, split, category)
            dst_path = os.path.join(PROCESSED_DATA_DIR, split, category)
            
            if not os.path.exists(src_path): continue

            files = os.listdir(src_path)
            print(f"-> Đang xử lý: {split}/{category} ({len(files)} ảnh)")
            
            for file_name in files:
                if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')): continue
                
                try:
                    file_src = os.path.join(src_path, file_name)
                    img = cv2.imread(file_src)
                    if img is None: continue
                    
                    clean_img = full_pipeline_process(img, is_augmentation=False)
                    cv2.imwrite(os.path.join(dst_path, file_name), clean_img)
                    
                    if split == 'train':
                        base_name = os.path.splitext(file_name)[0]
                        ext = os.path.splitext(file_name)[1]
                        
                        if category == 'NORMAL':
                            transforms_to_apply = TRANSFORMS
                        else:
                            transforms_to_apply = [t for t in TRANSFORMS if t[1] in ['rot', 'shift']]
                            
                        for func, suffix in transforms_to_apply:
                            aug_img = full_pipeline_process(img, is_augmentation=True, transform_func=func)
                            
                            new_name = f"{base_name}_{suffix}{ext}"
                            cv2.imwrite(os.path.join(dst_path, new_name), aug_img)
                            
                except Exception as e:
                    print(f"Lỗi file {file_name}: {e}")

    print("\n=== HOÀN TẤT ===")
    print(f"Dữ liệu đã sẵn sàng tại {PROCESSED_DATA_DIR}")

if __name__ == "__main__":
    main()