# Project Timeline & Tasks

> **Mới vào dự án?** Đọc [GETTING_STARTED.md](GETTING_STARTED.md) trước để biết bắt đầu từ đâu!

# Project Timeline & Tasks

> **Mới vào dự án?** Đọc [GETTING_STARTED.md](GETTING_STARTED.md) trước để biết bắt đầu từ đâu!

## Iteration 1 (27/11 - 04/12): Data & Notebook Setup

### Week 1: Data Collection & Training Prep

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i1w1** | Quang Duy | Data Collection | Thu thập dữ liệu từ Kaggle, loại bỏ ảnh lỗi/trùng/sai format | 29/11 |
| **i1w2** | Quang Duy | Preprocessing | Resize 224x224, normalize, cải thiện chất lượng | 04/12 |
| **i1w3** | Quang Duy | Augmentation & Split | Data augmentation, chia train/val/test | 04/12 |
| **i1w4** | Quốc Anh | CNN Notebook Setup | Chuẩn bị CNN.ipynb cho Kaggle training | 04/12 |
| **i1w5** | Tấn Lộc | ResNet Notebook Setup | Chuẩn bị ResNet.ipynb cho Kaggle training | 04/12 |
| **i1w6** | Quang Duy | Dataset Verification | Kiểm tra số lượng, format, bàn giao dataset | 04/12 |

### Deliverables
- Dataset đã xử lý (train/val/test)
- CNN.ipynb sẵn sàng train
- ResNet.ipynb sẵn sàng train
- Báo cáo preprocessing

---

## Iteration 2 (04/12 - 11/12): Training & Streamlit App

### Week 2: Model Training & Web App Development

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i2w1** | Quang Duy | Streamlit App Setup | Tạo app.py, custom UI/UX, CSS styling | 11/12 |
| **i2w2** | Quốc Anh | CNN Training on Kaggle | Train CNN, tune hyperparameters, save model | 11/12 |
| **i2w3** | Tấn Lộc | ResNet50 Training on Kaggle | Fine-tune ResNet50, save model | 11/12 |
| **i2w4** | Quang Duy | Streamlit Model Loading | Load models, image preprocessing logic | 11/12 |
| **i2w5** | Quốc Anh | CNN Model Optimization | Hyperparameter tuning, evaluation | 11/12 |

### Deliverables
- Streamlit app hoạt động
- CNN model (.h5)
- ResNet50 model (.h5)
- Training reports (accuracy, loss curves)

---

## Iteration 3 (11/12 - 18/12): Testing & Deployment

### Week 3: Model Comparison & Deployment

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i3w1** | Quang Duy | Streamlit Deployment | Deploy lên Streamlit Cloud hoặc local | 18/12 |
| **i3w2** | Quốc Anh | CNN Testing | Test cases, confusion matrix, evaluation | 18/12 |
| **i3w3** | Tấn Lộc | ResNet50 Testing | Test cases, confusion matrix, evaluation | 18/12 |
| **i3w4** | Tấn Lộc | Model Comparison | So sánh CNN vs ResNet50, viết báo cáo | 18/12 |
| **i3w5** | Quang Duy | Documentation | User guide, deployment guide | 18/12 |
| **i3w6** | All | Final Testing | End-to-end testing, bug fixes | 18/12 |

### Deliverables
- Deployed Streamlit app
- Model comparison report
- Testing report
- User documentation
- Demo ready

---

## Chi tiết công việc từng người

### Nguyễn Văn Quang Duy - Data & Deployment

**Iteration 1 (27/11 - 04/12):**
- [ ] Thu thập dataset từ Kaggle
- [ ] Loại bỏ ảnh lỗi, trùng, sai format
- [ ] Resize, normalize, cải thiện chất lượng
- [ ] Data augmentation
- [ ] Chia train/val/test
- [ ] Verify dataset cuối cùng
- [ ] Viết báo cáo preprocessing

**Iteration 2 (04/12 - 11/12):**
- [ ] Setup Streamlit app structure
- [ ] Tạo UI với st.file_uploader, model selector
- [ ] Custom CSS styling (green/red themes)
- [ ] Load models với @st.cache_resource
- [ ] Image preprocessing logic (resize, normalize)
- [ ] Test app với mock models

**Iteration 3 (11/12 - 18/12):**
- [ ] Deploy lên Streamlit Cloud
- [ ] Viết User Guide
- [ ] Viết Deployment Guide
- [ ] Fix bugs từ testing
- [ ] Support team

---

### Nguyễn Đặng Quốc Anh - CNN Model

**Iteration 1 (27/11 - 04/12):**
- [ ] Setup Kaggle account
- [ ] Chuẩn bị CNN.ipynb
- [ ] Test notebook locally (không train)
- [ ] Upload lên Kaggle, add dataset
- [ ] Verify GPU access

**Iteration 2 (04/12 - 11/12):**
- [ ] Train CNN trên Kaggle (GPU T4 x2)
- [ ] Hyperparameter tuning
- [ ] Save model (cnn_best.h5)
- [ ] Evaluation metrics
- [ ] Download model về local
- [ ] Test với Streamlit app

**Iteration 3 (11/12 - 18/12):**
- [ ] CNN testing với test set
- [ ] Confusion matrix
- [ ] Error analysis
- [ ] Model comparison (với Tấn Lộc)
- [ ] Testing & bug fixing

---

### Nguyễn Đình Tấn Lộc - ResNet50 & Comparison

**Iteration 1 (27/11 - 04/12):**
- [ ] Setup Kaggle account
- [ ] Chuẩn bị ResNet.ipynb
- [ ] Test notebook locally
- [ ] Upload lên Kaggle, add dataset
- [ ] Verify GPU access

**Iteration 2 (04/12 - 11/12):**
- [ ] Fine-tune ResNet50 trên Kaggle
- [ ] Hyperparameter tuning
- [ ] Save model (resnet50_best.h5)
- [ ] Evaluation metrics
- [ ] Download model về local
- [ ] Test với Streamlit app

**Iteration 3 (11/12 - 18/12):**
- [ ] ResNet50 testing với test set
- [ ] Confusion matrix
- [ ] So sánh CNN vs ResNet50:
  - Accuracy comparison
  - Training time
  - Inference time
  - Confusion matrices
- [ ] Viết báo cáo comparison (docs/model_comparison_report.md)
- [ ] Final testing
- [ ] Demo preparation

---

## Status Tracking

### Iteration 1: In Progress (27/11 - 04/12)
- Data Collection & Preprocessing
- CNN/ResNet Notebook Setup

### Iteration 2: Waiting (04/12 - 11/12)
- Chờ dataset từ Iteration 1
- Model training on Kaggle
- Streamlit app development

### Iteration 3: Waiting (11/12 - 18/12)
- Chờ models từ Iteration 2
- Testing, comparison & deployment

---

## Quick Links

**Iteration 1 Tasks:**
- [Quang Duy](tasks/ITERATION1_QUANGDUY.md)
- [Quốc Anh](tasks/ITERATION1_QUOCANH.md)
- [Tấn Lộc](tasks/ITERATION1_TANLOC.md)

**Iteration 2 Tasks:**
- [Quang Duy](tasks/ITERATION2_QUANGDUY.md)
- [Quốc Anh](tasks/ITERATION2_QUOCANH.md)
- [Tấn Lộc](tasks/ITERATION2_TANLOC.md)

**Iteration 3 Tasks:**
- [Quang Duy](tasks/ITERATION3_QUANGDUY.md)
- [Quốc Anh](tasks/ITERATION3_QUOCANH.md)
- [Tấn Lộc](tasks/ITERATION3_TANLOC.md)

---

## Weekly Meetings

**Mục đích:** Sync progress, resolve blockers

- **End of Week 1 (04/12):**
  - Review dataset preprocessing
  - Review CNN/ResNet notebooks
  - Plan Iteration 2

- **End of Week 2 (11/12):**
  - Demo Streamlit app
  - Demo trained models
  - Plan testing & comparison

- **End of Week 3 (18/12):**
  - Demo full system
  - Review comparison report
  - Final demo preparation
