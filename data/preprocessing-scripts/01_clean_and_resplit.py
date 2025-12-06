import os
import shutil
import hashlib
import cv2
import numpy as np
import random
from glob import glob
from sklearn.model_selection import GroupShuffleSplit 

RAW_DATA_DIR = "data/raw/chest_xray"
INTERIM_DATA_DIR = "data/interim"
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

def get_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def extract_patient_id(filename):
    parts = filename.split('_')
    if len(parts) > 1 and parts[0].startswith('person'):
        return parts[0]
    return filename 

def clean_and_resplit():
    print(f"=== BẮT ĐẦU QUY TRÌNH LÀM SẠCH & CHIA (GROUP SPLIT) ===")
    
    if os.path.exists(INTERIM_DATA_DIR):
        shutil.rmtree(INTERIM_DATA_DIR)
    
    all_data = {'NORMAL': [], 'PNEUMONIA': []}
    seen_hashes_train = set()
    
    print("--- Đang quét Train/Val (Tách ID bệnh nhân)... ---")
    
    for split in ['train', 'val']:
        for label in ['NORMAL', 'PNEUMONIA']:
            path = os.path.join(RAW_DATA_DIR, split, label)
            if not os.path.exists(path): continue
            
            files = os.listdir(path)
            for f in files:
                if not f.lower().endswith(('.jpg', '.jpeg', '.png')): continue
                full_path = os.path.join(path, f)
                
                try:
                    with open(full_path, 'rb') as _: pass
                except:
                    print(f"[Train-Corrupt] Bỏ qua: {f}")
                    continue

                # Check trùng lặp
                file_hash = get_md5(full_path)
                if file_hash in seen_hashes_train: continue
                seen_hashes_train.add(file_hash)
                
                p_id = extract_patient_id(f)
                all_data[label].append({'path': full_path, 'filename': f, 'patient_id': p_id})

    print(f"Số lượng ảnh Train/Val hợp lệ:")
    print(f"- NORMAL: {len(all_data['NORMAL'])}")
    print(f"- PNEUMONIA: {len(all_data['PNEUMONIA'])}")

    print("\n--- Đang chia Train/Val (90/10) theo Patient ID... ---")
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=SEED)
    
    for label in ['NORMAL', 'PNEUMONIA']:
        items = all_data[label]
        groups = [item['patient_id'] for item in items]
        
        train_idx, val_idx = next(splitter.split(items, groups=groups))
        
        for split_name, idx_list in [('train', train_idx), ('val', val_idx)]:
            target_dir = os.path.join(INTERIM_DATA_DIR, split_name, label)
            os.makedirs(target_dir, exist_ok=True)
            for i in idx_list:
                item = items[i]
                shutil.copy2(item['path'], os.path.join(target_dir, item['filename']))

    print("\n--- Đang xử lý tập TEST (Lọc lỗi cơ bản)... ---")
    
    for label in ['NORMAL', 'PNEUMONIA']:
        src_dir = os.path.join(RAW_DATA_DIR, 'test', label)
        dst_dir = os.path.join(INTERIM_DATA_DIR, 'test', label)
        os.makedirs(dst_dir, exist_ok=True)
        
        if not os.path.exists(src_dir): continue
        
        files = os.listdir(src_dir)
        test_seen_hashes = set()
        
        for f in files:
            if not f.lower().endswith(('.jpg', '.jpeg', '.png')): continue
            full_path = os.path.join(src_dir, f)
            
            try:
                img = cv2.imread(full_path)
                if img is None:
                    print(f"[Test-Corrupt] Bỏ file hỏng: {f}")
                    continue
                if img.shape[0] < 50 or img.shape[1] < 50:
                    print(f"[Test-Small] Bỏ file quá nhỏ: {f}")
                    continue
            except: continue
            
            file_hash = get_md5(full_path)
            if file_hash in test_seen_hashes:
                print(f"[Test-Duplicate] Bỏ file trùng: {f}")
                continue
            test_seen_hashes.add(file_hash)
            
            shutil.copy2(full_path, os.path.join(dst_dir, f))

    print("\n=== HOÀN TẤT ===")
    print(f"Dữ liệu sạch đã được lưu tại: {INTERIM_DATA_DIR}")

if __name__ == "__main__":
    clean_and_resplit()