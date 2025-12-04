import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np

# Cấu hình đường dẫn
RAW_DATA_PATH = "./data/raw/chest_xray/train"  # Đứng từ folder scripts nhìn ra

def inspect_image_sizes():
    print("--- BẮT ĐẦU KIỂM TRA KÍCH THƯỚC ẢNH ---")
    dimensions = []
    categories = ['NORMAL', 'PNEUMONIA']
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Lỗi: Không tìm thấy đường dẫn {RAW_DATA_PATH}")
        return

    for category in categories:
        folder_path = os.path.join(RAW_DATA_PATH, category)
        files = os.listdir(folder_path)
        print(f"Đang quét {category}: {len(files)} ảnh...")
        
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    with Image.open(os.path.join(folder_path, file_name)) as img:
                        dimensions.append((img.width, img.height, category))
                except:
                    pass
    
    # Vẽ biểu đồ và lưu lại thay vì show()
    widths = [x[0] for x in dimensions]
    heights = [x[1] for x in dimensions]
    labels = [x[2] for x in dimensions]
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=widths, y=heights, hue=labels, alpha=0.5)
    plt.title("Phân bố kích thước ảnh")
    plt.plot([0, 3000], [0, 3000], 'r--')
    
    output_file = "data/reports/size_distribution.png"
    plt.savefig(output_file)
    print(f"Đã lưu biểu đồ tại: {output_file}")

if __name__ == "__main__":
    inspect_image_sizes()