import os
import shutil
import hashlib
import cv2
import numpy as np
import random
import re
from sklearn.model_selection import GroupShuffleSplit

# Cấu hình
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data/processed/chest_xray"))
INTERIM_DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data/interim"))
SEED = 42

random.seed(SEED)
np.random.seed(SEED)


def get_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


# Trích patient id từ filename; ví dụ:
# - "person100_bacteria_475.jpeg" -> "person100"
# - "patient123_left.png" -> "patient123"
# - nếu không khớp mẫu, trả về phần trước dấu chấm (tên không chứa đường dẫn)
def extract_patient_id(filename):
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    m = re.match(r'^(person\d+|patient\d+|p\d+)', name, flags=re.IGNORECASE)
    if m:
        return m.group(1).lower()
    # fallback: nếu không có định dạng chuẩn, lấy prefix trước dấu '_' nếu có
    if '_' in name:
        return name.split('_')[0].lower()
    return name.lower()


def clean_and_resplit():
    print("Bắt đầu: làm sạch và chia lại dữ liệu (group split)")

    if os.path.exists(INTERIM_DATA_DIR):
        shutil.rmtree(INTERIM_DATA_DIR)

    all_data = {'NORMAL': [], 'PNEUMONIA': []}
    seen_hashes_train = set()

    # Quét train và val nguồn để gom ảnh, loại bỏ file corrupt và trùng
    for split in ['train', 'val']:
        for label in ['NORMAL', 'PNEUMONIA']:
            src_dir = os.path.join(RAW_DATA_DIR, split, label)
            if not os.path.exists(src_dir):
                continue

            for fname in os.listdir(src_dir):
                if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                full_path = os.path.join(src_dir, fname)

                # kiểm tra đọc file
                try:
                    with open(full_path, 'rb'):
                        pass
                except Exception:
                    print(f"[Skip-Corrupt] {full_path}")
                    continue

                file_hash = get_md5(full_path)
                if file_hash is None:
                    print(f"[Skip-HashError] {full_path}")
                    continue
                if file_hash in seen_hashes_train:
                    continue
                seen_hashes_train.add(file_hash)

                p_id = extract_patient_id(fname)
                all_data[label].append({'path': full_path, 'filename': fname, 'patient_id': p_id})

    print("Số lượng ảnh thu được (train+val source):")
    print(f"- NORMAL: {len(all_data['NORMAL'])}")
    print(f"- PNEUMONIA: {len(all_data['PNEUMONIA'])}")

    # Chia theo patient id: train 90% / val 10%
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=SEED)

    for label in ['NORMAL', 'PNEUMONIA']:
        items = all_data[label]
        if len(items) == 0:
            print(f"[Warn] Nhãn {label} không có ảnh nguồn, bỏ qua.")
            continue

        groups = [it['patient_id'] for it in items]
        unique_groups = set(groups)
        if len(unique_groups) < 2:
            # Không đủ group để split theo nhóm — fallback: random split trên ảnh
            print(f"[Warn] Không đủ patient group cho nhãn {label}. Thực hiện split ngẫu nhiên trên ảnh.")
            indices = np.arange(len(items))
            np.random.shuffle(indices)
            cutoff = int(len(indices) * 0.9)
            train_idx = indices[:cutoff]
            val_idx = indices[cutoff:]
        else:
            # chuẩn hóa X thành index array; gọi split với groups
            X = np.arange(len(items))
            try:
                train_idx, val_idx = next(splitter.split(X, groups=groups))
            except Exception as e:
                print(f"[Error] Split thất bại cho nhãn {label}: {e}")
                # fallback: random split
                indices = np.arange(len(items))
                np.random.shuffle(indices)
                cutoff = int(len(indices) * 0.9)
                train_idx = indices[:cutoff]
                val_idx = indices[cutoff:]

        for split_name, idx_list in [('train', train_idx), ('val', val_idx)]:
            target_dir = os.path.join(INTERIM_DATA_DIR, split_name, label)
            os.makedirs(target_dir, exist_ok=True)
            for i in idx_list:
                it = items[int(i)]
                shutil.copy2(it['path'], os.path.join(target_dir, it['filename']))

    # Xử lý test: lọc file corrupt, file quá nhỏ, loại trùng lặp
    for label in ['NORMAL', 'PNEUMONIA']:
        src_dir = os.path.join(RAW_DATA_DIR, 'test', label)
        dst_dir = os.path.join(INTERIM_DATA_DIR, 'test', label)
        os.makedirs(dst_dir, exist_ok=True)
        if not os.path.exists(src_dir):
            continue

        test_seen_hashes = set()
        for fname in os.listdir(src_dir):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            full_path = os.path.join(src_dir, fname)

            try:
                img = cv2.imread(full_path)
                if img is None:
                    print(f"[Test-Corrupt] {full_path}")
                    continue
                if img.shape[0] < 50 or img.shape[1] < 50:
                    print(f"[Test-Small] {full_path}")
                    continue
            except Exception:
                print(f"[Test-ReadError] {full_path}")
                continue

            file_hash = get_md5(full_path)
            if file_hash is None:
                print(f"[Test-HashError] {full_path}")
                continue
            if file_hash in test_seen_hashes:
                print(f"[Test-Duplicate] {full_path}")
                continue
            test_seen_hashes.add(file_hash)

            shutil.copy2(full_path, os.path.join(dst_dir, fname))

    print("Hoàn tất. Dữ liệu sạch đã lưu tại:", INTERIM_DATA_DIR)


if __name__ == "__main__":
    clean_and_resplit()
