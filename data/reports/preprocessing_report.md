# Báo cáo Tiền xử lý Dữ liệu (Data Preprocessing Report)

**Dự án:** Pneumonia Detection using Deep Learning
**Người thực hiện:** Nguyễn Văn Quang Duy
**Ngày cập nhật:** 27/11/2025

---

## 1. Tổng quan về Tập dữ liệu
Dữ liệu được sử dụng là tập ảnh **Chest X-Ray Images (Pneumonia)** từ Kaggle.
- **Loại dữ liệu:** Ảnh X-quang lồng ngực (Grayscale).
- **Nhãn (Labels):** 2 lớp
  - `NORMAL`: Phổi bình thường.
  - `PNEUMONIA`: Viêm phổi (do vi khuẩn hoặc virus).
- **Cấu trúc gốc:** Chia sẵn thành 3 tập `train`, `val`, `test`.

---

## 2. Phân tích Dữ liệu (Exploratory Data Analysis - EDA)

Trước khi tiến hành xử lý, chúng tôi đã thực hiện các bước kiểm tra dữ liệu để đưa ra chiến lược phù hợp.

### 2.1. Phân bố kích thước ảnh
- **Phương pháp:** Vẽ biểu đồ Scatter Plot giữa Chiều rộng (Width) và Chiều cao (Height).
- **Quan sát:**
  - Kích thước ảnh không đồng nhất, dao động lớn (từ ~400px đến >2500px).
  - Đa số ảnh có tỷ lệ **Chiều rộng > Chiều cao** (ảnh chữ nhật ngang).
  - Điểm dữ liệu nằm lệch xa so với đường chéo tỷ lệ 1:1 (hình vuông).
- **Kết luận:** Việc Resize trực tiếp về hình vuông (ví dụ 224x224) sẽ gây méo ảnh (biến dạng lồng ngực), làm sai lệch đặc trưng hình học. Cần sử dụng phương pháp **Padding**.

### 2.2. Phân tích Histogram & Độ sáng
- **Phương pháp:** So sánh Histogram trung bình của tập `NORMAL` và `PNEUMONIA`.
- **Quan sát:** Hai đường biểu đồ Histogram gần như trùng khít nhau ở dải cường độ sáng (50-250).
- **Kết luận:**
  - Sự khác biệt giữa hai lớp không nằm ở độ sáng tổng thể (Global Intensity).
  - Không thể chỉ dựa vào Cân bằng Histogram toàn cục (Global Histogram Equalization).
  - Cần áp dụng kỹ thuật làm nổi bật đặc trưng cục bộ như **CLAHE**.

### 2.3. Ảnh trung bình (Average Image)
- **Phương pháp:** Cộng gộp và tính trung bình cộng pixel của toàn bộ ảnh trong mỗi lớp.
- **Quan sát:** Ảnh trung bình của `PNEUMONIA` có độ "mờ đục" (whiter/cloudier) cao hơn ở vùng phổi so với `NORMAL`. Điều này phù hợp với đặc điểm y học của bệnh viêm phổi (hiện tượng đông đặc/thâm nhiễm phổi).

---

## 3. Quy trình Tiền xử lý (Preprocessing Pipeline)

Dựa trên kết quả phân tích, quy trình xử lý chuẩn áp dụng cho từng ảnh như sau:

1.  **Chuyển đổi Grayscale:** Đưa tất cả ảnh về 1 kênh màu (nếu có ảnh RGB) để đồng nhất đầu vào.
2.  **Resize with Padding (Quan trọng):**
    - **Mục đích:** Giữ nguyên tỷ lệ khung hình (Aspect Ratio), tránh làm méo phổi.
    - **Thực hiện:** Thu nhỏ ảnh sao cho cạnh lớn nhất bằng **256 pixel**. Phần dư thừa được điền màu đen (Padding value = 0).
    - **Kích thước đích:** `256 x 256`.
3.  **Cân bằng Histogram thích nghi (CLAHE):**
    - **Tham số:** `clipLimit=2.0`, `tileGridSize=(8, 8)`.
    - **Mục đích:** Tăng cường độ tương phản cục bộ, giúp làm rõ các chi tiết xương sườn và các đốm mờ viêm phổi mà không làm nhiễu ảnh như phương pháp cân bằng thông thường.

---

## 4. Chiến lược Tăng cường Dữ liệu (Data Augmentation)

Do số lượng ảnh gốc hạn chế (nguy cơ Overfitting) và mất cân bằng nhẹ, chúng tôi áp dụng **Offline Augmentation** (sinh ra file ảnh mới và lưu trữ) cho tập **TRAIN**.

Mỗi ảnh gốc trong tập Train sẽ sinh ra **6 biến thể** mới, bao gồm:

1.  **Xoay (Rotation):** Ngẫu nhiên $\pm 10^{\circ}$.
2.  **Lật (Horizontal Flip):** Lật ngang ảnh (mô phỏng thay đổi hướng chụp).
3.  **Zoom:** Phóng to ngẫu nhiên 10-20% vào vùng trung tâm.
4.  **Dịch chuyển (Shift):** Dịch sang các hướng tối đa 10%.
5.  **Làm mờ (Gaussian Blur):** Kernel $3\times3$ hoặc $5\times5$ (Mô phỏng ảnh bị rung/mất nét).
6.  **Làm nét (Sharpening):** Sử dụng Laplacian kernel để làm nổi bật cạnh và chi tiết xương.

**Kết quả:** Tập dữ liệu Train tăng lên gấp **7 lần** (1 ảnh gốc + 6 ảnh biến thể), giúp mô hình học được tính bất biến (invariance) tốt hơn.

---

## 5. Đặc tả Dữ liệu đầu ra (Output Specifications)

Dữ liệu sau xử lý được lưu tại thư mục `data/processed/` và sẵn sàng để huấn luyện mô hình.

*   **Format:** `.jpeg`
*   **Color Space:** Grayscale (1 Channel).
*   **Resolution:** `256 x 256`.
*   **Lưu ý cho Team Model (Quốc Anh & Tấn Lộc):**
    *   **CNN Model:** Input shape nên thiết lập là `(256, 256, 1)`.
    *   **ResNet-50 Model:** ResNet yêu cầu 3 kênh màu. Khi load data, cần thực hiện bước lặp kênh: `np.stack((img,)*3, axis=-1)` hoặc cấu hình `ImageDataGenerator` để convert sang RGB.
    *   **Data Split:** Sử dụng đúng cấu trúc thư mục `train`, `val`, `test` đã tạo.

---

## 6. Kết luận
Giai đoạn Data Preprocessing đã hoàn tất. Dữ liệu đã được làm sạch, chuẩn hóa kích thước và tăng cường số lượng đáng kể. Các kỹ thuật xử lý ảnh (CLAHE, Sharpening, Padding) đã được áp dụng đúng theo định hướng của môn học để tối ưu hóa đặc trưng cho bài toán phân loại X-quang.

***