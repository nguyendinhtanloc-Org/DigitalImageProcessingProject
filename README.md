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
┌─────────────┐      HTTP/REST      ┌──────────────┐      Python API     ┌─────────────┐
│   ReactJS   │ ──────────────────> │ Spring Boot  │ ─────────────────> │   Models    │
│  Frontend   │ <────────────────── │   Backend    │ <───────────────── │ (CNN/ResNet)│
└─────────────┘      JSON Response  └──────────────┘     Prediction     └─────────────┘
```

---

## Cấu trúc dự án

```
DigitalImageProcessingProject/
│
├── backend/                           # Spring Boot API - Quang Duy
│   ├── src/main/java/com/pneumonia/
│   │   ├── controller/               # API endpoints
│   │   ├── service/                  # Business logic
│   │   ├── dto/                      # Request/Response objects
│   │   ├── config/                   # Configuration
│   │   └── exception/                # Error handling
│   ├── src/main/resources/
│   ├── pom.xml
│   ├── Dockerfile
│   ├── README.md
│   └── TASKS.md                      # Chi tiết công việc Quang Duy
│
├── frontend/                          # ReactJS - Quốc Anh & Tấn Lộc
│   ├── src/
│   │   ├── components/               # UI components
│   │   ├── pages/                    # Pages
│   │   ├── services/                 # API calls
│   │   └── utils/                    # Helpers
│   ├── package.json
│   ├── Dockerfile
│   ├── README.md
│   └── TASKS.md                      # Chi tiết công việc Quốc Anh
│
├── model-service/                     # Python Flask API - Shared
│   ├── app/
│   │   ├── routes/                   # API endpoints
│   │   ├── services/                 # Model inference
│   │   └── utils/                    # Helpers
│   ├── models/                       # Trained models (.h5)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── notebooks/                         # Jupyter notebooks - Kaggle
│   ├── CNN.ipynb                     # Quốc Anh - CNN training
│   ├── ResNet.ipynb                  # Tấn Lộc - ResNet50 training
│   ├── evaluation/
│   │   ├── CNN_evaluation.ipynb
│   │   └── ResNet_evaluation.ipynb
│   ├── comparison/
│   │   └── Model_Comparison.ipynb    # Tấn Lộc - So sánh models
│   └── README.md
│
├── data/                              # Dataset & Preprocessing - Quang Duy
│   ├── preprocessing-scripts/        # Python scripts tiền xử lý
│   │   ├── 01_data_inspection.py
│   │   ├── 02_data_cleaning.py
│   │   ├── 03_preprocessing.py
│   │   ├── 04_augmentation.py
│   │   └── 05_split_dataset.py
│   ├── reports/                      # Báo cáo tiền xử lý
│   │   ├── data_inspection_report.md
│   │   └── preprocessing_report.md
│   ├── README.md
│   └── TASKS_QUANGDUY.md            # Chi tiết công việc
│
├── models/                            # Saved models
│   ├── cnn_best.h5                   # Từ Quốc Anh
│   ├── resnet50_best.h5              # Từ Tấn Lộc
│   └── README.md
│
├── deployment/                        # Docker deployment - Tấn Lộc
│   ├── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── README.md
│
├── docs/                              # Tài liệu
│   ├── model_comparison_report.md    # Tấn Lộc
│   ├── USER_GUIDE.md                 # Tấn Lộc
│   ├── report.pdf                    # Báo cáo cuối
│   └── slides.pptx                   # Thuyết trình
│
├── .gitignore
├── CONTRIBUTING.md
├── TASKS_TANLOC.md                   # Chi tiết công việc Tấn Lộc
└── README.md
```

---

## Công nghệ sử dụng

### Backend
- **Java 17+**
- **Spring Boot 3.x** (REST API)
- **Maven** (Build tool)
- **Swagger/OpenAPI** (API Documentation)

### Frontend
- **ReactJS 18.x**
- **TailwindCSS** (Styling)
- **Axios** (HTTP Client)
- **Vite** (Build tool)

### AI/ML
- **Python 3.8+**
- **TensorFlow/Keras** hoặc **PyTorch**
- **ResNet-50** (Transfer Learning)
- **Grad-CAM** (Visualization)
- **NumPy, Pandas, Matplotlib**

### Dataset
- [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) từ Kaggle

---

## Cài đặt và chạy dự án

### Prerequisites

Đảm bảo bạn đã cài đặt:
- **Java 17+** ([Download](https://www.oracle.com/java/technologies/downloads/))
- **Maven 3.8+** ([Download](https://maven.apache.org/download.cgi))
- **Node.js 18+** và **npm** ([Download](https://nodejs.org/))
- **Python 3.8+** và **pip** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))

### Bước 1: Clone repository

```bash
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject
```

### Bước 2: Train Models trên Kaggle

**Lưu ý:** Việc training models được thực hiện trên Kaggle Notebooks để tận dụng GPU miễn phí.

1. **Upload notebooks lên Kaggle:**
   - Truy cập [Kaggle](https://www.kaggle.com/)
   - Tạo notebook mới hoặc upload `notebooks/CNN.ipynb` và `notebooks/ResNet.ipynb`

2. **Thêm dataset:**
   - Add dataset: [Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

3. **Chạy training:**
   - Bật GPU: Settings > Accelerator > GPU T4 x2
   - Run all cells
   - Training time: ~2-3 giờ cho mỗi model

4. **Download trained models:**
   - Sau khi train xong, download file `.h5` từ Kaggle
   - Lưu vào thư mục `models/`

### Bước 3: Setup Backend (Spring Boot)

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

Backend sẽ chạy tại: `http://localhost:8080`  
Swagger UI: `http://localhost:8080/swagger-ui.html`

### Bước 4: Setup Frontend (ReactJS)

```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:5173`

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