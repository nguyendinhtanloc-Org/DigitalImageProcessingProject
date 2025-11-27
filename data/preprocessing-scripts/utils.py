import cv2
import numpy as np

# Cấu hình chung cho toàn bộ dự án
TARGET_SIZE = 256

def resize_with_padding(image, target_size=TARGET_SIZE):
    """
    Resize ảnh về target_size x target_size mà không làm méo ảnh.
    Phần dư sẽ được điền màu đen (Padding).
    Dùng chung cho cả Training và Inference.
    """
    old_size = image.shape[:2]
    ratio = float(target_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    
    # Resize giữ nguyên tỷ lệ
    # INTER_AREA tốt cho thu nhỏ ảnh (downsampling)
    image = cv2.resize(image, (new_size[1], new_size[0]), interpolation=cv2.INTER_AREA)
    
    # Tính toán padding để đưa về hình vuông
    delta_w = target_size - new_size[1]
    delta_h = target_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    
    # Thêm viền đen
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

def apply_clahe(image):
    """Áp dụng cân bằng histogram thích nghi (CLAHE)"""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def process_image_pipeline(img):
    """
    Quy trình chuẩn: Gray -> Resize+Padding -> CLAHE
    Dùng cho script tạo dữ liệu Training (trả về ảnh uint8 để lưu file).
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    img = resize_with_padding(img, target_size=TARGET_SIZE)
    img = apply_clahe(img)
    return img

def preprocess_image_for_model(image_path_or_array, model_type='cnn'):
    """
    HÀM NÀY DÙNG CHO WEB/BACKEND (INFERENCE)
    Input: Đường dẫn file ảnh HOẶC numpy array (từ upload)
    Output: Numpy array 4 chiều chuẩn hóa (1, 256, 256, C) giá trị [0, 1]
    """
    # 1. Đọc ảnh
    if isinstance(image_path_or_array, str):
        img = cv2.imread(image_path_or_array)
    else:
        img = image_path_or_array

    if img is None:
        raise ValueError("Không thể đọc được ảnh!")

    # 2. Chuyển Gray (Bắt buộc)
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img

    # 3. Resize + Padding + CLAHE (Tái sử dụng các hàm cơ bản)
    img_processed = resize_with_padding(img_gray, target_size=TARGET_SIZE)
    img_processed = apply_clahe(img_processed)

    # 4. Chuẩn hóa giá trị về [0, 1] (Quan trọng cho Model)
    img_normalized = img_processed.astype('float32') / 255.0

    # 5. Xử lý kênh màu (Channel)
    if model_type == 'resnet':
        # ResNet cần 3 kênh giả lập
        img_final = np.stack((img_normalized,)*3, axis=-1) # (256, 256, 3)
    else:
        # CNN thường cần 1 kênh
        img_final = np.expand_dims(img_normalized, axis=-1) # (256, 256, 1)

    # 6. Thêm chiều Batch (Batch Dimension) -> (1, 256, 256, C)
    img_batch = np.expand_dims(img_final, axis=0)
    
    return img_batch