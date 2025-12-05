# Iteration 2 - Quốc Anh (04/12 - 11/12)

**Mục tiêu:** Train CNN trên Kaggle

---

## Checklist

### Ngày 1-2 (04-05/12): Kaggle Setup

- [ ] Upload `notebooks/CNN.ipynb` lên Kaggle
- [ ] Add dataset: "chest xray pneumonia"
- [ ] Enable GPU: T4 x2
- [ ] Test chạy vài epochs

### Ngày 3-5 (06-08/12): Training

- [ ] Train full model (~2-3 giờ)
  - Epochs: 20-30
  - Batch size: 32
  - Callbacks: ModelCheckpoint, EarlyStopping

- [ ] Monitor training:
  - Training accuracy
  - Validation accuracy
  - Loss curves

### Ngày 6-7 (09-11/12): Evaluation & Export

- [ ] Evaluate trên test set
  - Accuracy > 88%
  - Confusion matrix
  - Classification report

- [ ] Save model: `cnn_best.h5`
- [ ] Download về `models/cnn_best.h5`
- [ ] Test load model local
- [ ] Commit model (Git LFS hoặc Drive link)

---

## Output

- `models/cnn_best.h5` - Trained CNN model
- Training report với metrics

---

**Expected:** Accuracy ~88-92%  
**Next:** Iteration 3 - Tích hợp vào Streamlit
