# Project Timeline & Tasks

> **Mới vào dự án?** Đọc [GETTING_STARTED.md](GETTING_STARTED.md) trước để biết bắt đầu từ đâu!

## Iteration 1 (27/11 - 04/12): Data & Frontend Setup

### Week 1: Data Collection & Basic UI

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i1w1** | Quang Duy | Data Collection | Thu thập dữ liệu từ Kaggle, loại bỏ ảnh lỗi/trùng/sai format | 29/11 |
| **i1w2** | Quang Duy | Preprocessing | Resize 224x224, normalize, cải thiện chất lượng | 04/12 |
| **i1w3** | Quang Duy | Augmentation & Split | Data augmentation, chia train/val/test | 04/12 |
| **i1w4** | Quốc Anh | Website Skeleton | React + TailwindCSS: layout, upload form, result display | 04/12 |
| **i1w5** | Tấn Lộc | JS Preview Logic | Preview ảnh, placeholder kết quả | 04/12 |
| **i1w6** | Quang Duy | Dataset Verification | Kiểm tra số lượng, format, bàn giao dataset | 04/12 |

### Deliverables
- Dataset đã xử lý (train/val/test)
- Frontend basic UI
- Báo cáo preprocessing

---

## Iteration 2 (04/12 - 11/12): API & Models

### Week 2: Backend API & Model Training

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i2w1** | Quang Duy | API Setup | Spring Boot API: `/predict/cnn`, `/predict/resnet50`, Swagger | 11/12 |
| **i2w2** | Quốc Anh | CNN Training | Design CNN, train trên Kaggle, save model | 11/12 |
| **i2w3** | Tấn Lộc | ResNet50 Fine-tune | Load pretrained, fine-tune, save model | 11/12 |
| **i2w4** | Quang Duy | API Unit Test | Test với Postman, xử lý lỗi | 11/12 |
| **i2w5** | Quốc Anh | React Components | Upload, preview, result display components với mock data | 11/12 |

### Deliverables
- Spring Boot API hoạt động
- CNN model (.h5)
- ResNet50 model (.h5)
- React components với mock data
- API documentation (Swagger)

---

## Iteration 3 (11/12 - 18/12): Integration & Polish

### Week 3: Full Integration & Testing

| Task ID | Owner | Task | Chi tiết | Deadline |
|---------|-------|------|----------|----------|
| **i3w1** | Quốc Anh | Connect Frontend-API | React + Axios call Spring Boot API, hiển thị kết quả | 18/12 |
| **i3w2** | Tấn Lộc | End-to-End Integration | Tích hợp full pipeline, fix bugs | 18/12 |
| **i3w3** | Quang Duy | API Refinement | Tối ưu API, xử lý edge cases | 18/12 |
| **i3w4** | Tấn Lộc + Quốc Anh | Model Comparison | So sánh CNN vs ResNet50, viết báo cáo | 18/12 |
| **i3w5** | Quốc Anh | UI Polishing | Hoàn thiện UI/UX, responsive design | 18/12 |
| **i3w6** | Quang Duy | Swagger Documentation | Hoàn thiện API docs | 18/12 |

### Deliverables
- Website hoạt động hoàn chỉnh
- Model comparison report
- API documentation đầy đủ
- Testing report
- Demo ready

---

## Chi tiết công việc từng người

### Nguyễn Văn Quang Duy

**Iteration 1 (27/11 - 04/12):**
- [ ] Thu thập dataset từ Kaggle
- [ ] Loại bỏ ảnh lỗi, trùng, sai format
- [ ] Resize, normalize, cải thiện chất lượng
- [ ] Data augmentation
- [ ] Chia train/val/test
- [ ] Verify dataset cuối cùng
- [ ] Viết báo cáo preprocessing

**Iteration 2 (04/12 - 11/12):**
- [ ] Setup Spring Boot project
- [ ] Tạo endpoints: `/predict/cnn`, `/predict/resnet50`
- [ ] Xử lý upload ảnh
- [ ] Gọi Python model service
- [ ] Test API với Postman
- [ ] Setup Swagger UI

**Iteration 3 (11/12 - 18/12):**
- [ ] Tối ưu API performance
- [ ] Xử lý edge cases
- [ ] Fix bugs từ integration
- [ ] Hoàn thiện Swagger docs
- [ ] Support team integration

---

### Nguyễn Đặng Quốc Anh

**Iteration 1 (27/11 - 04/12):**
- [ ] Setup React + Vite + TailwindCSS
- [ ] Tạo layout cơ bản (Header, Footer)
- [ ] Component upload ảnh
- [ ] Component hiển thị kết quả
- [ ] Mock data testing

**Iteration 2 (04/12 - 11/12):**
- [ ] Train CNN trên Kaggle
- [ ] Save model (.h5)
- [ ] Evaluation metrics
- [ ] Tạo React components chính:
  - UploadImage
  - ResultDisplay
  - ModelSelector
- [ ] Test với mock API

**Iteration 3 (11/12 - 18/12):**
- [ ] Connect React với backend API
- [ ] Handle loading states
- [ ] Error handling
- [ ] UI/UX polishing
- [ ] Responsive design
- [ ] Model comparison (với Tấn Lộc)
- [ ] Testing & bug fixing

---

### Nguyễn Đình Tấn Lộc

**Iteration 1 (27/11 - 04/12):**
- [ ] Setup frontend preview logic
- [ ] Image preview component
- [ ] Placeholder kết quả
- [ ] Chuẩn bị ResNet notebook

**Iteration 2 (04/12 - 11/12):**
- [ ] Fine-tune ResNet50 trên Kaggle
- [ ] Save model (.h5)
- [ ] Evaluation metrics
- [ ] Chuẩn bị Python Flask service (nếu cần)

**Iteration 3 (11/12 - 18/12):**
- [ ] Tích hợp Frontend ↔ Backend
- [ ] End-to-end testing
- [ ] Fix bugs integration
- [ ] So sánh CNN vs ResNet50:
  - Accuracy comparison
  - Confusion matrices
  - Training curves
  - Inference time
- [ ] Viết báo cáo comparison
- [ ] Final testing
- [ ] Demo preparation

---

## Status Tracking

### Iteration 1: ✓ In Progress (27/11 - 04/12)
- Data Collection
- Preprocessing
- Frontend Setup

### Iteration 2: Waiting (04/12 - 11/12)
- Chờ dataset từ Iteration 1
- Backend API development
- Model training

### Iteration 3: Waiting (11/12 - 18/12)
- Chờ API & models từ Iteration 2
- Integration & testing

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
  - Review dataset
  - Review frontend UI
  - Plan Iteration 2

- **End of Week 2 (11/12):**
  - Demo API
  - Demo models
  - Plan integration

- **End of Week 3 (18/12):**
  - Demo full system
  - Review comparison report
  - Final preparation
