import os
import cv2
import numpy as np
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns

# Xác định đường dẫn tuyệt đối dựa trên vị trí file script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../processed/chest_xray"))
REPORT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../reports/after_processed"))

os.makedirs(REPORT_DIR, exist_ok=True)


def calculate_md5(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def scan_dataset(root_dir):
    records = []
    print("Đang quét dữ liệu từ:", os.path.abspath(root_dir))

    for split in ['train', 'test', 'val']:
        for label in ['NORMAL', 'PNEUMONIA']:
            folder = os.path.join(root_dir, split, label)
            if not os.path.exists(folder):
                continue

            for file_name in os.listdir(folder):
                if not file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue

                file_path = os.path.join(folder, file_name)
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    print("Không đọc được:", file_path)
                    continue

                h, w = img.shape
                records.append({
                    'filepath': file_path,
                    'filename': file_name,
                    'split': split,
                    'label': label,
                    'width': w,
                    'height': h,
                    'mean_intensity': np.mean(img),
                    'std_intensity': np.std(img),
                    'md5_hash': calculate_md5(file_path)
                })

    return pd.DataFrame(records)


df = scan_dataset(DATA_DIR)
print("Tổng số ảnh quét được:", len(df))

if df.empty:
    print("Không tìm thấy ảnh trong thư mục dữ liệu. Vui lòng kiểm tra lại DATA_DIR.")
    exit()

df.to_csv(os.path.join(REPORT_DIR, "dataset_statistics.csv"), index=False)

duplicate_count = df.duplicated(subset=['md5_hash']).sum()
print("Số lượng file trùng lặp:", duplicate_count)

if duplicate_count > 0:
    dup_list = df[df.duplicated(subset=['md5_hash'], keep=False)]
    dup_list.to_csv(os.path.join(REPORT_DIR, "duplicates_list.csv"), index=False)

print("Đang vẽ biểu đồ phân bố...")

plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x='split', hue='label', palette='viridis')

for container in ax.containers:
    ax.bar_label(container, padding=3, fontsize=10, fmt='%d')

plt.title("Phân bố dữ liệu theo tập và nhãn")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "class_balance_with_numbers.png"))
plt.close()

print("Đang phân tích ngoại lai...")

dark_count = (df['mean_intensity'] < 20).sum()
bright_count = (df['mean_intensity'] > 230).sum()
flat_count = (df['std_intensity'] == 0).sum()

print("Ảnh quá tối (<20):", dark_count)
print("Ảnh quá sáng (>230):", bright_count)
print("Ảnh không có độ lệch chuẩn (std=0):", flat_count)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='label', y='mean_intensity')
plt.title("Phân bố giá trị độ sáng")

plt.subplot(1, 2, 2)
sns.boxplot(data=df, x='label', y='std_intensity')
plt.title("Phân bố độ tương phản")

plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "intensity_boxplot.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='width', y='height', hue='label', alpha=0.5)
plt.title("Phân bố kích thước ảnh")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "size_distribution.png"))
plt.close()

print("Hoàn tất. Báo cáo đã được lưu trong:", REPORT_DIR)
