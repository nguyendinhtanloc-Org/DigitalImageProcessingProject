# Hướng dẫn bắt đầu dự án

Đọc file này TRƯỚC KHI BẮT ĐẦU CODE!

## Bước 1: Hiểu cấu trúc dự án

```
GETTING_STARTED.md  ← Bạn đang đọc file này
    ↓
README.md           ← Tổng quan dự án
    ↓
TIMELINE.md         ← Timeline 3 tuần (ai làm gì, khi nào)
    ↓
CONTRIBUTING.md     ← Quy tắc commit, branch, code
    ↓
tasks/              ← Chi tiết công việc theo iteration
```

## Bước 2: Đọc theo thứ tự

1. **README.md** (5 phút) - Hiểu dự án làm gì, tech stack
2. **TIMELINE.md** (10 phút) - Xem timeline 3 tuần, deadline
3. **CONTRIBUTING.md** (10 phút) - Học Git Flow, commit conventions
4. **tasks/ITERATION[N]_[TÊN].md** (10 phút) - Chi tiết task tuần này

## Bước 3: Setup môi trường

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Kaggle Account** (để train models)

### Clone project

```bash
git clone https://github.com/nguyendinhtanloc-Org/DigitalImageProcessingProject.git
cd DigitalImageProcessingProject
```

## Hướng dẫn từng thành viên

### Nguyễn Văn Quang Duy - Data & Deployment

**Iteration 1: Data Preprocessing**

```bash
# Tạo branch
git checkout -b feature/data-preprocessing

# Setup Python environment
cd data
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài packages
pip install -r requirements.txt

# Download dataset từ Kaggle
# Link: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
# Lưu vào: data/raw/

# Chạy preprocessing
cd preprocessing-scripts
python 01_data_inspection.py
python 02_data_cleaning.py
python 03_preprocessing.py
python 04_augmentation.py
python 05_split_dataset.py
```

Chi tiết: `tasks/ITERATION1_QUANGDUY.md`

---

**Iteration 2: Streamlit App**

```bash
git checkout -b feature/streamlit-app

cd app
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Customize app.py theo yêu cầu
# Test với mock models (tạm thời)
streamlit run app.py
```

Chi tiết: `tasks/ITERATION2_QUANGDUY.md`

---

**Iteration 3: Deployment**

```bash
# Deploy lên Streamlit Cloud hoặc local
# Viết tài liệu hướng dẫn sử dụng
```

Chi tiết: `tasks/ITERATION3_QUANGDUY.md`

---

### Nguyễn Đặng Quốc Anh - CNN Model

**Iteration 1: Notebook Setup**

```bash
# Tạo branch
git checkout -b feature/cnn-notebook

# Chuẩn bị notebook
cd notebooks
# Edit CNN.ipynb

# Test local (không train, chỉ check code)
jupyter notebook CNN.ipynb
```

Chi tiết: `tasks/ITERATION1_QUOCANH.md`

---

**Iteration 2: CNN Training**

```bash
# Upload CNN.ipynb lên Kaggle
# Add dataset: Chest X-Ray Pneumonia
# Enable GPU: T4 x2
# Train ~2-3 giờ

# Download model
# Lưu vào: models/cnn_best.h5
```

Chi tiết: `tasks/ITERATION2_QUOCANH.md`

---

**Iteration 3: Testing & Evaluation**

```bash
# Tạo notebook testing
# Confusion matrix, metrics
# Báo cáo kết quả
```

Chi tiết: `tasks/ITERATION3_QUOCANH.md`

---

### Nguyễn Đình Tấn Lộc - ResNet50 & Comparison

**Iteration 1: Notebook Setup**

```bash
git checkout -b feature/resnet-notebook

cd notebooks
# Edit ResNet.ipynb

jupyter notebook ResNet.ipynb
```

Chi tiết: `tasks/ITERATION1_TANLOC.md`

---

**Iteration 2: ResNet50 Training**

```bash
# Upload ResNet.ipynb lên Kaggle
# Fine-tune ResNet50
# Train ~2-3 giờ

# Download: models/resnet50_best.h5
```

Chi tiết: `tasks/ITERATION2_TANLOC.md`

---

**Iteration 3: Model Comparison**

```bash
# So sánh CNN vs ResNet50
# Viết báo cáo: docs/model_comparison_report.md
# Final report
```

Chi tiết: `tasks/ITERATION3_TANLOC.md`

---

## Checklist từng tuần

### Week 1 (27/11 - 04/12)

- [ ] Quang Duy: Dataset preprocessing xong
- [ ] Quốc Anh: CNN notebook chuẩn bị xong
- [ ] Tấn Lộc: ResNet notebook chuẩn bị xong

### Week 2 (04/12 - 11/12)

- [ ] Quang Duy: Streamlit app xong
- [ ] Quốc Anh: CNN model trained
- [ ] Tấn Lộc: ResNet50 model trained

### Week 3 (11/12 - 18/12)

- [ ] Quang Duy: Deployment xong
- [ ] Quốc Anh: CNN testing xong
- [ ] Tấn Lộc: Model comparison xong

## Quy trình hàng ngày

### Trước khi code

```bash
git checkout develop
git pull origin develop
git checkout -b feature/ten-feature
```

### Trong khi code

```bash
# Commit thường xuyên
git add .
git commit -m "feat: mô tả ngắn"
```

### Sau khi xong

```bash
git push origin feature/ten-feature
# Tạo Pull Request trên GitHub
```

## Lưu ý quan trọng

### Không commit:
- `data/raw/*` - Dataset (quá lớn)
- `data/processed/*` - Processed data
- `models/*.h5` - Models (dùng Google Drive)
- `venv/`, `__pycache__/`

### File quan trọng:
1. README.md
2. TIMELINE.md
3. CONTRIBUTING.md
4. tasks/ITERATION[N]_[TÊN].md

## Câu hỏi thường gặp

**Q: Bắt đầu từ đâu?**  
A: Đọc README.md → TIMELINE.md → Task file của bạn

**Q: Commit message viết sao?**  
A: `feat(scope): mô tả` (xem CONTRIBUTING.md)

**Q: Train model ở đâu?**  
A: Kaggle (GPU miễn phí)

**Q: Streamlit app chạy ở đâu?**  
A: Local (CPU đủ cho inference)

---

Cập nhật: 27/11/2025

