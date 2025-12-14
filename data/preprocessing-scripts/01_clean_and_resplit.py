import os
import shutil
import hashlib
import cv2
import numpy as np
import random
from glob import glob
from sklearn.model_selection import GroupShuffleSplit

# --- CẤU HÌNH ---
RAW_DATA_DIR = "data/raw/chest_xray"
INTERIM_DATA_DIR = "data/interim"
SEED = 42

# Tỉ lệ chia (80% Train - 10% Val - 10% Test)
TEST_SIZE = 0.1
VAL_SIZE = 0.1111  # Vì sau khi tách 10% Test, còn lại 90%. Lấy 10% của tổng nghĩa là 1/9 của phần còn lại.

random.seed(SEED)
np.random.seed(SEED)

def get_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except: return None

def extract_patient_id(filename):
    # Tách ID: person1946_bacteria... -> person1946
    parts = filename.split('_')
    if len(parts) > 1 and parts[0].startswith('person'):
        return parts[0]
    return filename 

def clean_and_resplit():
    print(f"=== BẮT ĐẦU GỘP TẤT CẢ VÀ CHIA LẠI (80-10-10) ===")
    
    if os.path.exists(INTERIM_DATA_DIR):
        shutil.rmtree(INTERIM_DATA_DIR)
    
    # 1. Thu thập TẤT CẢ ảnh từ mọi ngóc ngách
    all_data = {'NORMAL': [], 'PNEUMONIA': []}
    seen_hashes = set()
    
    print("--- Đang quét và gộp toàn bộ dữ liệu (Train+Val+Test)... ---")
    
    # Duyệt qua cả 3 folder cũ
    for split in ['train', 'val', 'test']:
        for label in ['NORMAL', 'PNEUMONIA']:
            path = os.path.join(RAW_DATA_DIR, split, label)
            if not os.path.exists(path): continue
            
            files = os.listdir(path)
            for f in files:
                if not f.lower().endswith(('.jpg', '.jpeg', '.png')): continue
                full_path = os.path.join(path, f)
                
                # Check lỗi đọc file
                try:
                    with open(full_path, 'rb') as _: pass
                except:
                    print(f"[Corrupt] Bỏ qua: {f}")
                    continue

                # Check trùng lặp toàn cục
                file_hash = get_md5(full_path)
                if file_hash in seen_hashes: continue
                seen_hashes.add(file_hash)
                
                p_id = extract_patient_id(f)
                all_data[label].append({'path': full_path, 'filename': f, 'patient_id': p_id})

    print(f"Tổng số ảnh sạch thu được:")
    print(f"- NORMAL: {len(all_data['NORMAL'])}")
    print(f"- PNEUMONIA: {len(all_data['PNEUMONIA'])}")

    # 2. Chia dữ liệu theo ID Bệnh nhân
    print("\n--- Đang chia Train / Val / Test... ---")
    
    for label in ['NORMAL', 'PNEUMONIA']:
        items = all_data[label]
        groups = [item['patient_id'] for item in items]
        
        # Bước 1: Tách Test ra trước (10%)
        splitter_test = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=SEED)
        train_val_idx, test_idx = next(splitter_test.split(items, groups=groups))
        
        test_items = [items[i] for i in test_idx]
        train_val_items = [items[i] for i in train_val_idx]
        train_val_groups = [groups[i] for i in train_val_idx] # Update groups tương ứng
        
        # Bước 2: Tách Train và Val từ phần còn lại (Val lấy 11.11% của phần còn lại ~ 10% tổng)
        splitter_val = GroupShuffleSplit(n_splits=1, test_size=VAL_SIZE, random_state=SEED)
        train_idx, val_idx = next(splitter_val.split(train_val_items, groups=train_val_groups))
        
        train_items = [train_val_items[i] for i in train_idx]
        val_items = [train_val_items[i] for i in val_idx]
        
        # 3. Copy file vào thư mục đích
        for split_name, item_list in [('train', train_items), ('val', val_items), ('test', test_items)]:
            target_dir = os.path.join(INTERIM_DATA_DIR, split_name, label)
            os.makedirs(target_dir, exist_ok=True)
            
            for item in item_list:
                shutil.copy2(item['path'], os.path.join(target_dir, item['filename']))

    print("\n=== HOÀN TẤT ===")
    print(f"Dữ liệu (80/10/10) đã sẵn sàng tại: {INTERIM_DATA_DIR}")
    
    # In thống kê nhanh để kiểm tra
    for split in ['train', 'val', 'test']:
        n_norm = len(os.listdir(os.path.join(INTERIM_DATA_DIR, split, 'NORMAL')))
        n_pneu = len(os.listdir(os.path.join(INTERIM_DATA_DIR, split, 'PNEUMONIA')))
        total = n_norm + n_pneu
        print(f"- {split.upper()}: {total} ảnh (Norm: {n_norm}, Pneu: {n_pneu})")

if __name__ == "__main__":
    clean_and_resplit()