# Báo cáo Tiền xử lý Dữ liệu (Data Preprocessing Report)

**Dự án:** Pneumonia Detection using Deep Learning
**Người thực hiện:** Nguyễn Văn Quang Duy
**Ngày cập nhật:** 27/11/2024
**Trạng thái:** Hoàn tất Iteration 1

---

## 1. Tổng quan về Tập dữ liệu
Dữ liệu được sử dụng là tập ảnh **Chest X-Ray Images (Pneumonia)** từ Kaggle.
- **Loại dữ liệu:** Ảnh X-quang lồng ngực (Grayscale).
- **Nhãn (Labels):** 2 lớp
  - `NORMAL`: Phổi bình thường.
  - `PNEUMONIA`: Viêm phổi.
- **Vấn đề ban đầu:**
    - Mất cân bằng dữ liệu nghiêm trọng (Pneumonia gấp 3 lần Normal).
    - Tập Validation quá ít (16 ảnh).
    - Chất lượng ảnh không đồng đều (ánh sáng, độ tương phản).
    - Tồn tại ảnh trùng lặp (Duplicates) và ảnh lỗi (Outliers).

---

## 2. Quy trình Làm sạch & Tái cấu trúc (Cleaning & Resplit)

Trước khi xử lý ảnh, chúng tôi đã thực hiện dọn dẹp dữ liệu thô:

1.  **Loại bỏ Trùng lặp (De-duplication):** Sử dụng mã băm MD5 để phát hiện và xóa các ảnh trùng nhau trong cùng một tập.
2.  **Loại bỏ Ngoại lai (Outlier Removal):** Dựa trên phân tích thống kê Histogram:
    - Loại bỏ ảnh quá tối (`Mean Intensity < 40`).
    - Loại bỏ ảnh quá sáng/lóa (`Mean Intensity > 220`).
    - Loại bỏ ảnh lỗi tương phản (`Std Dev < 15`).
3.  **Chia lại tập dữ liệu (Resplit):**
    - Gộp tập `TRAIN` cũ và `VAL` cũ lại.
    - Chia lại theo tỷ lệ chuẩn: **90% Train** - **10% Val**.
    - **Tập TEST:** Giữ nguyên trạng từ Kaggle để đảm bảo tính khách quan khi đánh giá (Benchmark).

**Kết quả phân bố sau khi làm sạch:**
- Val set tăng từ 16 ảnh lên ~520 ảnh (Đủ tin cậy để đánh giá).

---

## 3. Pipeline Tiền xử lý Nâng cao (Advanced Preprocessing Pipeline)

Đây là quy trình xử lý áp dụng cho **từng bức ảnh** (cả lúc Train và lúc chạy Web App) để tối ưu hóa đặc trưng bệnh lý.

### Bước 1: Grayscale Conversion
- Chuyển tất cả ảnh về ảnh xám (1 kênh màu) để đồng nhất đầu vào.

### Bước 2: Resize with Padding (Quan trọng)
- **Kích thước đích:** `256 x 256`.
- **Kỹ thuật:** Thay vì cắt (crop) hoặc kéo dãn (stretch), chúng tôi thêm viền đen (padding) vào cạnh ngắn hơn để biến ảnh thành hình vuông.
- **Lý do:** Bảo toàn tỷ lệ hình học của tim và phổi, tránh làm méo mó cấu trúc giải phẫu.

### Bước 3: Gaussian Blur (Denoising)
- **Kỹ thuật:** Áp dụng bộ lọc làm mờ nhẹ (Kernel 3x3).
- **Lý do:** Loại bỏ nhiễu hạt (noise) tần số cao trước khi đưa vào các bước tăng cường cạnh, tránh việc nhiễu bị khuếch đại.

### Bước 4: Homomorphic Filtering (Miền tần số - Frequency Domain)
- **Kỹ thuật:** Chuyển ảnh sang miền tần số (Fourier Transform), áp dụng bộ lọc thông cao (High-pass) kết hợp xử lý Logarithm.
- **Tham số:** `gamma_L=0.5` (Giảm sáng nền), `gamma_H=1.5` (Tăng chi tiết cạnh).
- **Lý do:**
    - Khắc phục hiện tượng ánh sáng không đồng đều (Illumination correction).
    - Làm sắc nét các cạnh xương và mô phổi.

### Bước 5: CLAHE (Contrast Limited Adaptive Histogram Equalization)
- **Kỹ thuật:** Cân bằng histogram thích nghi cục bộ.
- **Tham số:** `ClipLimit=2.0`, `TileGridSize=(8,8)`.
- **Lý do:** Làm nổi bật các đám mờ, thâm nhiễm (đặc trưng của viêm phổi) vốn có độ tương phản thấp so với nền xương.

---

## 4. Chiến lược Tăng cường Dữ liệu (Data Augmentation)

Để giải quyết vấn đề **Mất cân bằng dữ liệu (Class Imbalance)** trong tập Train, chúng tôi áp dụng chiến lược tăng cường có trọng số (Weighted Augmentation).

**Chỉ áp dụng cho tập TRAIN:**

1.  **Lớp NORMAL (Thiểu số - Minor Class):**
    - Áp dụng **Full Augmentation (x7)**: 1 ảnh gốc sinh ra 6 biến thể.
    - Biến thể gồm: Xoay ($\pm 10^\circ$), Zoom (10-20%), Dịch chuyển (Shift), Làm mờ (Blur), Làm nét (Sharpen).
    - **Mục đích:** Tăng số lượng ảnh Normal lên tối đa để bắt kịp Pneumonia.

2.  **Lớp PNEUMONIA (Đa số - Major Class):**
    - Áp dụng **Partial Augmentation (x3)**: 1 ảnh gốc sinh ra 2 biến thể.
    - Biến thể gồm: Chỉ Xoay và Dịch chuyển.
    - **Mục đích:** Tăng nhẹ sự đa dạng nhưng kìm hãm số lượng để không lấn át Normal.

**Lưu ý:** Chúng tôi **KHÔNG** sử dụng phép lật ngang (Horizontal Flip) để tránh sai lệch giải phẫu tim/phổi (Đảo phủ tạng).

---

## 5. Kết quả & Hướng dẫn sử dụng (Handover Guide)

### Thống kê Dữ liệu cuối cùng (Final Statistics)
- **TRAIN:** ~19,000 ảnh (Tỷ lệ cân bằng Normal/Pneumonia xấp xỉ 1:1.2).
- **VAL:** ~520 ảnh.
- **TEST:** ~624 ảnh.

### Hướng dẫn cho Team Model (Quốc Anh & Tấn Lộc)
1.  **Dữ liệu:** Tải file `processed_data.zip` từ Drive chung và giải nén.
2.  **Input Shape:**
    - CNN: `(256, 256, 1)`
    - ResNet: Cần convert sang 3 kênh màu (RGB) khi load data.
3.  **Inference (Web App):**
    - Sử dụng hàm `preprocess_image_for_model` trong file `utils.py` để xử lý ảnh upload từ người dùng. Hàm này đảm bảo ảnh đầu vào Web giống 100% với ảnh đã được huấn luyện.

---
**Kết luận:** Dữ liệu đã Sạch - Cân bằng - Tối ưu hóa đặc trưng. Sẵn sàng cho giai đoạn Training.