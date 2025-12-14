import os
import cv2
import numpy as np
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "data/raw/chest_xray" # data/raw/chest_xray or data/processed
REPORT_DIR = "data/reports/before_processed" #data/reports/before_processed or after_processed

if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

def calculate_md5(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def scan_dataset(root_dir):
    data_records = []
    print(f"Đang quét dữ liệu từ: {root_dir}...")
    
    for split in ['train', 'test', 'val']:
        for label in ['NORMAL', 'PNEUMONIA']:
            folder_path = os.path.join(root_dir, split, label)
            if not os.path.exists(folder_path): continue
            
            files = os.listdir(folder_path)
            for file_name in files:
                if not file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                file_path = os.path.join(folder_path, file_name)
                try:
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        print(f"[Corrupt] Không đọc được: {file_path}")
                        continue
                        
                    h, w = img.shape
                    mean_intensity = np.mean(img)
                    std_intensity = np.std(img)
                    file_hash = calculate_md5(file_path)
                    
                    data_records.append({
                        'filepath': file_path,
                        'filename': file_name,
                        'split': split,
                        'label': label,
                        'width': w,
                        'height': h,
                        'mean_intensity': mean_intensity,
                        'std_intensity': std_intensity,
                        'md5_hash': file_hash
                    })
                except Exception as e:
                    print(f"[Error] Lỗi xử lý {file_name}: {e}")

    return pd.DataFrame(data_records)


df = scan_dataset(DATA_DIR)
print(f"Tổng số ảnh quét được: {len(df)}")

df.to_csv(os.path.join(REPORT_DIR, "dataset_statistics.csv"), index=False)

duplicates = df[df.duplicated(subset=['md5_hash'], keep=False)]
num_dupes = df.duplicated(subset=['md5_hash']).sum()
print(f"Số lượng file trùng lặp: {num_dupes}")

if num_dupes > 0:
    duplicates.to_csv(os.path.join(REPORT_DIR, "duplicates_list.csv"), index=False)

print("Đang vẽ biểu đồ phân bố...")
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x='split', hue='label', palette='viridis')

for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=3, fontsize=10, fmt='%d')

plt.title(f"Phân bố dữ liệu trong {DATA_DIR}")
plt.ylim(0, df.groupby(['split', 'label']).size().max() * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "class_balance_with_numbers.png"))
plt.close()

print("Đang phân tích ngoại lai...")
dark_cnt = len(df[df['mean_intensity'] < 20])
bright_cnt = len(df[df['mean_intensity'] > 230])
flat_cnt = len(df[df['std_intensity'] == 0])

print(f"- Ảnh quá tối (<20): {dark_cnt}")
print(f"- Ảnh quá sáng (>230): {bright_cnt}")
print(f"- Ảnh lỗi (Std=0): {flat_cnt}")

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='label', y='mean_intensity')
plt.title("Phân bố độ sáng (Mean Intensity)")

plt.subplot(1, 2, 2)
sns.boxplot(data=df, x='label', y='std_intensity')
plt.title("Phân bố độ tương phản (Std Dev)")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "intensity_boxplot.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='width', y='height', hue='label', alpha=0.5)
plt.title("Phân bố kích thước ảnh")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "size_distribution.png"))
plt.close()

print(f"\n=== HOÀN TẤT ===")
print(f"Toàn bộ báo cáo và biểu đồ đã được lưu vào: {os.path.abspath(REPORT_DIR)}")