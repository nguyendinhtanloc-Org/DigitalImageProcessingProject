# Iteration 2 - Quốc Anh (04/12 - 11/12)

**Mục tiêu:** CNN Training + React Components nâng cao

---

## PART 1: CNN Training (4 ngày)

### Ngày 1-2 (04-05/12): Kaggle Setup & Architecture

- [ ] Upload `notebooks/CNN.ipynb` lên Kaggle
- [ ] Add dataset: "chest xray pneumonia"
- [ ] Enable GPU: T4 x2
- [ ] Design CNN architecture:
  ```python
  Conv2D(32) → MaxPool → Conv2D(64) → MaxPool
  → Conv2D(128) → Flatten → Dense(512) → Dense(2)
  ```
- [ ] Setup data pipeline:
  - ImageDataGenerator
  - Augmentation
  - Batch size: 32

### Ngày 3-4 (06-08/12): Training & Evaluation

- [ ] Train model (~2-3 giờ)
  - Epochs: 20-30
  - Callbacks: ModelCheckpoint, EarlyStopping
  - Monitor: val_accuracy

- [ ] Evaluate:
  - Test accuracy > 88%
  - Confusion matrix
  - Classification report

- [ ] Save model: `cnn_best.h5`
- [ ] Download về `models/cnn_best.h5`

---

## PART 2: React Components (3 ngày)

### Ngày 5-6 (09-10/12): Enhanced Components

- [ ] Update `UploadImage.jsx`:
  - Drag & drop support
  - Image validation
  - Better preview
  - Clear/reset button

- [ ] Update `ResultDisplay.jsx`:
  - Animated confidence bar
  - Color coding (green/red)
  - Better typography
  - Share/download result

- [ ] Create `HistoryPanel.jsx`:
  - localStorage lưu predictions
  - List previous results
  - Click to view detail

### Ngày 7 (11/12): Integration & Demo

- [ ] Test components với mock data
- [ ] Responsive design polish
- [ ] Commit code
- [ ] **Demo CNN model & UI cho team**

---

## Output Deliverables

- `models/cnn_best.h5` - Trained CNN model
- Enhanced React components
- Training report với accuracy, loss curves

---

## Expected Metrics

- Training accuracy: ~90-92%
- Validation accuracy: ~88-90%
- Test accuracy: ~88-92%

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 3 - Connect real API
