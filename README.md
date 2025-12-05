# Dự án Phân loại Ảnh X-quang Phổi - Pneumonia Detection

> **BẮT ĐẦU TẠI ĐÂY:** [GETTING_STARTED.md](GETTING_STARTED.md) - Hướng dẫn cho thành viên mới

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cài đặt và chạy dự án](#cài-đặt-và-chạy-dự-án)
- [Quy trình làm việc](#quy-trình-làm-việc)
- [Đóng góp](#đóng-góp)
- [Team members](#team-members)

---

## Giới thiệu

Dự án **Pneumonia Detection** sử dụng Deep Learning để phân loại ảnh X-quang phổi thành hai lớp:
- **Normal** (Bình thường)
- **Pneumonia** (Viêm phổi)

### Mục tiêu
- So sánh hiệu suất giữa **CNN tự xây dựng** và **Transfer Learning (ResNet-50)**
- Xây dựng ứng dụng web cho phép upload ảnh và dự đoán kết quả
- Trực quan hóa vùng quan trọng bằng **Grad-CAM**

---

## Tính năng

- **Hai mô hình AI**: CNN custom và ResNet-50
- **Upload ảnh X-quang** và nhận kết quả dự đoán realtime
- **Hiển thị confidence score** (độ tin cậy)
- **Grad-CAM visualization** - xem vùng mô hình chú ý
- **RESTful API** với Spring Boot
- **Responsive UI** với ReactJS + TailwindCSS
- **API Documentation** với Swagger UI

---

## Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────┐
│                 Streamlit Web App                   │
│   (Python + Streamlit + TensorFlow)                 │
│                                                      │
│   - Upload ảnh X-quang                              │
│   - Chọn model (CNN / ResNet50)                     │
│   - Hiển thị kết quả + Confidence                   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│              Trained Models (local)                  │
│   - models/cnn_best.h5                              │
│   - models/resnet50_best.h5                         │
└─────────────────────────────────────────────────────┘
```

**Training:** Models được train trên Kaggle (GPU miễn phí)  
**Inference:** Streamlit app chạy local (CPU đủ)

---

## Cấu trúc dự án

```
DigitalImageProcessingProject/
│
├── app/                              # Streamlit Web App
│   ├── app.py                       # Main application
│   ├── utils/                       # Helper functions
│   ├── requirements.txt             # Python dependencies
│   └── README.md
│
├── data/                             # Dataset & Preprocessing - Quang Duy
│   ├── raw/                         # Dataset gốc (KHÔNG commit)
│   ├── processed/                   # Dataset đã xử lý (KHÔNG commit)
│   ├── preprocessing-scripts/       # Python scripts
│   │   ├── 01_data_inspection.py
│   │   ├── 02_data_cleaning.py
│   │   ├── 03_preprocessing.py
│   │   ├── 04_augmentation.py
│   │   └── 05_split_dataset.py
│   ├── reports/                     # Báo cáo preprocessing
│   ├── requirements.txt
│   └── README.md
│
├── notebooks/                        # Training Notebooks - Kaggle
│   ├── CNN.ipynb                    # Quốc Anh - CNN training
│   ├── ResNet.ipynb                 # Tấn Lộc - ResNet50 training
│   └── Model_Comparison.ipynb       # Tấn Lộc - So sánh models
│
├── models/                           # Trained Models
│   ├── cnn_best.h5                  # Từ Quốc Anh
│   ├── resnet50_best.h5             # Từ Tấn Lộc
│   └── README.md
│
├── tasks/                            # Task files theo iteration
│   ├── ITERATION1_*.md
│   ├── ITERATION2_*.md
│   └── ITERATION3_*.md
│
├── docs/                             # Tài liệu
│   └── model_comparison_report.md   # Tấn Lộc
│
├── .gitignore
├── GETTING_STARTED.md
├── TIMELINE.md
├── CONTRIBUTING.md
└── README.md
```

---

## Công nghệ sử dụng

### Web App
- **Python 3.8+**
- **Streamlit** (Web framework)
- **TensorFlow/Keras** (Load & run models)
- **Pillow, OpenCV** (Image processing)

### AI/ML
- **TensorFlow/Keras** (Training)
- **CNN** (Custom architecture)
- **ResNet-50** (Transfer Learning)
- **NumPy, Pandas, Matplotlib**

### Training Platform
- **Kaggle Notebooks** (GPU T4 x2 miễn phí)
- **Jupyter Notebook** (Local development)

### Dataset
- [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) từ Kaggle

---

## Cài đặt và chạy dự án

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Kaggle Account** (để train models)

### Bước 1: Clone repository

```bash
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject
```

### Bước 2: Train Models trên Kaggle

**Training được thực hiện trên Kaggle (GPU miễn phí)**

1. Upload `notebooks/CNN.ipynb` và `notebooks/ResNet.ipynb` lên Kaggle
2. Add dataset: [Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
3. Enable GPU: T4 x2
4. Run training (~2-3 giờ mỗi model)
5. Download models: `cnn_best.h5` và `resnet50_best.h5`
6. Lưu vào thư mục `models/`

### Bước 3: Chạy Streamlit App

```bash
cd app

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài packages
pip install -r requirements.txt

# Chạy app
streamlit run app.py
```

App sẽ mở tại: **http://localhost:8501**

---

## Quy trình làm việc

### Branching Strategy

Dự án sử dụng **Git Flow**:

```
main          ────────────────────────────────────
                    ↑                    ↑
develop       ──────┴────────────────────┴─────────
                ↑         ↑         ↑
feature/*     ──┴──  ─────┴──  ─────┴──
```

- `main`: Code production, chỉ merge từ `develop` khi release
- `develop`: Code development chính
- `feature/*`: Branches cho từng tính năng mới
- `hotfix/*`: Sửa lỗi khẩn cấp trên `main`

### Workflow

1. **Tạo branch mới từ develop:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/ten-tinh-nang
   ```

2. **Code và commit thường xuyên:**
   ```bash
   git add .
   git commit -m "feat: thêm chức năng upload ảnh"
   ```

3. **Push và tạo Pull Request:**
   ```bash
   git push origin feature/ten-tinh-nang
   ```

4. **Review và merge vào develop**

### Commit Convention

Tuân theo **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Tính năng mới
- `fix`: Sửa bug
- `docs`: Cập nhật tài liệu
- `style`: Format code (không ảnh hưởng logic)
- `refactor`: Refactor code
- `test`: Thêm/sửa tests
- `chore`: Cập nhật build tools, dependencies

**Ví dụ:**
```bash
git commit -m "feat(frontend): thêm component upload ảnh X-ray"
git commit -m "fix(backend): sửa lỗi CORS khi call API"
git commit -m "docs: cập nhật hướng dẫn cài đặt trong README"
```

---

## Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết quy tắc chi tiết về:
- Code style
- Pull Request process
- Code review guidelines

---

## Timeline & Iterations

Dự án chia thành 3 iterations (3 tuần):

- **Iteration 1 (27/11 - 04/12):** Data Collection & Frontend Setup
- **Iteration 2 (04/12 - 11/12):** API Development & Model Training  
- **Iteration 3 (11/12 - 18/12):** Integration & Testing

Chi tiết đầy đủ: [TIMELINE.md](TIMELINE.md)

---

## Team Members & Phân công

| Thành viên | MSSV | Iteration 1<br>(27/11 - 04/12) | Iteration 2<br>(04/12 - 11/12) | Iteration 3<br>(11/12 - 18/12) |
|------------|------|-------------------------------|-------------------------------|-------------------------------|
| **Nguyễn Văn Quang Duy** | 22520309 | Data preprocessing<br>Dataset verification | Spring Boot API<br>Swagger setup | API optimization<br>Documentation |
| **Nguyễn Đặng Quốc Anh** | 22520022 | React UI skeleton<br>TailwindCSS setup | CNN training<br>React components | Frontend-Backend connect<br>UI polishing |
| **Nguyễn Đình Tấn Lộc** | 22520788 | Preview logic<br>Placeholder UI | ResNet50 fine-tune<br>Flask service | End-to-end integration<br>Model comparison |

Xem chi tiết tasks từng người: [TIMELINE.md](TIMELINE.md)

### Luồng công việc

```
Week 1 (27/11-04/12):  Data + UI Setup
         ↓
Week 2 (04/12-11/12):  API + Models Training
         ↓
Week 3 (11/12-18/12):  Integration + Testing
         ↓
      Demo Ready!
```

---

## License

Dự án này được phát hành dưới [MIT License](LICENSE).

---

## Liên hệ

Nếu có thắc mắc, vui lòng liên hệ qua:
- Email: team@example.com
- Issues: [GitHub Issues](https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject/issues)

---

**Đồ án Digital Image Processing - Năm học 2024-2025**