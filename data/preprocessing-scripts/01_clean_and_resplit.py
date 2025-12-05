import os
import shutil
import hashlib
import cv2
import numpy as np
import random
from glob import glob

DATA_DIR = "data/raw/chest_xray"

THRESH_MEAN_LOW = 40
THRESH_MEAN_HIGH = 220
THRESH_STD_LOW = 15

def get_md5(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def clean_and_resplit():
    print("=== BẮT ĐẦU DỌN DẸP VÀ CHIA LẠI DỮ LIỆU ===")
    
    all_files = {'NORMAL': [], 'PNEUMONIA': []}
    
    for split in ['train', 'val']:
        for label in ['NORMAL', 'PNEUMONIA']:
            path = os.path.join(DATA_DIR, split, label)
            if not os.path.exists(path): continue
            
            files = glob(os.path.join(path, "*.jpeg")) + glob(os.path.join(path, "*.jpg")) + glob(os.path.join(path, "*.png"))
            all_files[label].extend(files)

    print(f"Tổng số ảnh thu thập (Train + Val cũ):")
    print(f"- NORMAL: {len(all_files['NORMAL'])}")
    print(f"- PNEUMONIA: {len(all_files['PNEUMONIA'])}")

    clean_files = {'NORMAL': [], 'PNEUMONIA': []}
    seen_hashes = set()
    removed_count = 0
    
    print("\n--- Đang kiểm tra chất lượng ảnh... ---")
    
    for label in ['NORMAL', 'PNEUMONIA']:
        for file_path in all_files[label]:
            try:
                file_hash = get_md5(file_path)
                if file_hash in seen_hashes:
                    os.remove(file_path)
                    removed_count += 1
                    continue
                seen_hashes.add(file_hash)
                
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    os.remove(file_path)
                    continue
                    
                mean_val = np.mean(img)
                std_val = np.std(img)
                
                if (mean_val < THRESH_MEAN_LOW) or \
                   (mean_val > THRESH_MEAN_HIGH) or \
                   (std_val < THRESH_STD_LOW):
                    os.remove(file_path)
                    removed_count += 1
                    continue
                
                clean_files[label].append(file_path)
                
            except Exception as e:
                print(f"Lỗi {file_path}: {e}")

    print(f"Đã xóa vĩnh viễn {removed_count} ảnh kém chất lượng/trùng lặp.")

    print("\n--- Đang chia lại Train/Val (90/10)... ---")
    
    for label in ['NORMAL', 'PNEUMONIA']:
        files = clean_files[label]
        random.shuffle(files)
        
        n_total = len(files)
        n_val = int(n_total * 0.1)
        
        val_files = files[:n_val]
        train_files = files[n_val:]
        
        target_val_dir = os.path.join(DATA_DIR, 'val', label)
        os.makedirs(target_val_dir, exist_ok=True)
        for f in val_files:
            file_name = os.path.basename(f)
            dest = os.path.join(target_val_dir, file_name)
            if f != dest: shutil.move(f, dest)
            
        target_train_dir = os.path.join(DATA_DIR, 'train', label)
        os.makedirs(target_train_dir, exist_ok=True)
        for f in train_files:
            file_name = os.path.basename(f)
            dest = os.path.join(target_train_dir, file_name)
            if f != dest: shutil.move(f, dest)

    print("\n=== HOÀN TẤT ===")
    print("Cấu trúc thư mục raw đã được làm sạch và chuẩn hóa.")

if __name__ == "__main__":
    clean_and_resplit()