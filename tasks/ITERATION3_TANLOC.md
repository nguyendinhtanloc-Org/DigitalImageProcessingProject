# Iteration 3 - Tấn Lộc (11/12 - 18/12)

**Mục tiêu:** End-to-End Integration + Model Comparison + Docker

---

## PART 1: Integration Testing (3 ngày)

### Ngày 1-2 (11-12/12): Full Pipeline Test

- [ ] Test flow: Frontend → Backend → Model Service
- [ ] Verify:
  - Image upload từ React
  - Backend nhận file
  - Model service predict
  - Response hiển thị đúng

- [ ] Debug integration issues
- [ ] Test cả CNN & ResNet50
- [ ] Test error scenarios

### Ngày 3 (13/12): Bug Fixes

- [ ] Fix bugs phát hiện
- [ ] Optimize data flow
- [ ] Improve error handling
- [ ] Performance testing

---

## PART 2: Model Comparison (2 ngày)

### Ngày 4-5 (14-15/12): Comparison Report

- [ ] Create `notebooks/comparison/Model_Comparison.ipynb`
- [ ] Load both models:
  ```python
  cnn = load_model('models/cnn_best.h5')
  resnet = load_model('models/resnet50_best.h5')
  ```

- [ ] Compare metrics:
  - Accuracy, Precision, Recall, F1
  - Confusion matrices side-by-side
  - ROC curves
  - Inference time

- [ ] Visualizations:
  - Training/validation curves
  - Sample predictions
  - Error analysis

- [ ] Write report: `docs/model_comparison_report.md`

---

## PART 3: Docker Deployment (2 ngày)

### Ngày 6 (16/12): Docker Setup

- [ ] Create `deployment/docker-compose.yml`
- [ ] Test build:
  ```bash
  docker-compose build
  ```

- [ ] Test run:
  ```bash
  docker-compose up
  ```

- [ ] Verify all services:
  - Frontend: localhost:3000
  - Backend: localhost:8080
  - Model Service: localhost:5000

### Ngày 7 (17-18/12): Final Testing & Demo

- [ ] End-to-end test qua Docker
- [ ] Write deployment guide
- [ ] Create demo script
- [ ] **Final presentation**

---

## Output Deliverables

- Full system integration working
- Model comparison report
- Docker deployment ready
- Demo presentation

---

**Status:** TODO → DOING → DONE ✓
