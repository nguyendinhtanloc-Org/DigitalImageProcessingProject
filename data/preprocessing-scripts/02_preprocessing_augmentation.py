import os
import cv2
import numpy as np
import shutil
import random
from utils import process_image_pipeline

current_script_path = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(current_script_path, "..", "raw", "chest_xray")
PROCESSED_DATA_DIR = os.path.join(current_script_path, "..", "processed")

def do_rotate(image):
    rows, cols = image.shape
    angle = random.uniform(-10, 10)
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def do_zoom(image):
    zoom_factor = random.uniform(1.1, 1.2)
    h, w = image.shape
    new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)
    top = (h - new_h) // 2
    left = (w - new_w) // 2
    cropped = image[top:top+new_h, left:left+new_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

def do_shift(image):
    rows, cols = image.shape
    tx = random.uniform(-0.1, 0.1) * cols
    ty = random.uniform(-0.1, 0.1) * rows
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def do_blur(image):
    k_size = random.choice([3, 5])
    return cv2.GaussianBlur(image, (k_size, k_size), 0)

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

def main():
    if os.path.exists(PROCESSED_DATA_DIR):
        print(f"Đang xóa dữ liệu cũ tại {PROCESSED_DATA_DIR}...")
        shutil.rmtree(PROCESSED_DATA_DIR)

    for split in ['train', 'val', 'test']:
        for category in ['NORMAL', 'PNEUMONIA']:
            os.makedirs(os.path.join(PROCESSED_DATA_DIR, split, category), exist_ok=True)

    splits = ['train', 'val', 'test']
    categories = ['NORMAL', 'PNEUMONIA']

    print(f"Bắt đầu xử lý dữ liệu từ {RAW_DATA_DIR}...")
    print("Chiến lược: Train (Cân bằng Normal/Pneumonia); Val/Test (Giữ nguyên)")

    for split in splits:
        for category in categories:
            src_path = os.path.join(RAW_DATA_DIR, split, category)
            dst_path = os.path.join(PROCESSED_DATA_DIR, split, category)
            
            if not os.path.exists(src_path): 
                print(f"[Bỏ qua] Không tìm thấy thư mục nguồn: {src_path}")
                continue

            files = os.listdir(src_path)
            print(f"-> Đang xử lý: {split}/{category} ({len(files)} ảnh gốc)")
            
            for file_name in files:
                if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')): continue
                    
                try:
                    file_src = os.path.join(src_path, file_name)
                    img = cv2.imread(file_src)
                    if img is None: continue
                    
                    clean_img = process_image_pipeline(img)
                    
                    cv2.imwrite(os.path.join(dst_path, file_name), clean_img)
                    
                    if split == 'train':
                        base_name = os.path.splitext(file_name)[0]
                        ext = os.path.splitext(file_name)[1]
                        
                        if category == 'NORMAL':
                            selected_transforms = TRANSFORMS
                        else: 
                            selected_transforms = [t for t in TRANSFORMS if t[1] in ['rot', 'shift']]
                        
                        for func, suffix in selected_transforms:
                            aug_img = func(clean_img)
                            new_name = f"{base_name}_{suffix}{ext}"
                            cv2.imwrite(os.path.join(dst_path, new_name), aug_img)
                            
                except Exception as e:
                    print(f"Lỗi xử lý file {file_name}: {e}")

    print("\n=== HOÀN TẤT ===")
    print(f"Dữ liệu đã sẵn sàng tại {PROCESSED_DATA_DIR}")
    
    # In thống kê sơ bộ
    for split in splits:
        n_norm = len(os.listdir(os.path.join(PROCESSED_DATA_DIR, split, 'NORMAL')))
        n_pneu = len(os.listdir(os.path.join(PROCESSED_DATA_DIR, split, 'PNEUMONIA')))
        print(f"- {split.upper()}: NORMAL={n_norm}, PNEUMONIA={n_pneu}")

if __name__ == "__main__":
    main()