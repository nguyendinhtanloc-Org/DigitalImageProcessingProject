# Iteration 2 - Tấn Lộc (04/12 - 11/12)

**Mục tiêu:** Train ResNet50 trên Kaggle

---

## Checklist

### Ngày 1-2 (04-05/12): Kaggle Setup

- [ ] Upload `notebooks/ResNet.ipynb` lên Kaggle
- [ ] Add dataset
- [ ] Enable GPU: T4 x2
- [ ] Test chạy vài epochs

### Ngày 3-5 (06-08/12): Training

- [ ] Phase 1: Train top layers (10 epochs)
- [ ] Phase 2: Fine-tune (20 epochs)
  - Unfreeze last 50 layers
  - Learning rate: 0.0001

- [ ] Monitor training curves

### Ngày 6-7 (09-11/12): Evaluation & Export

- [ ] Evaluate trên test set
  - Accuracy > 92%
  - Confusion matrix
  - Compare với CNN

- [ ] Save model: `resnet50_best.h5`
- [ ] Download về `models/resnet50_best.h5`
- [ ] Test load model local
- [ ] Commit model

---

## Output

- `models/resnet50_best.h5` - Trained ResNet50 model
- Training report

---

**Expected:** Accuracy ~92-96%  
**Next:** Iteration 3 - Model Comparison
