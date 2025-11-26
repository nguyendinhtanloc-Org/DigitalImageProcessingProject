# Iteration 2 - Tấn Lộc (04/12 - 11/12)

**Mục tiêu:** ResNet50 Training + Flask Service (optional)

---

## PART 1: ResNet50 Training (5 ngày)

### Ngày 1-2 (04-05/12): Kaggle Setup & Transfer Learning

- [ ] Upload `notebooks/ResNet.ipynb` lên Kaggle
- [ ] Add dataset + Enable GPU
- [ ] Load pretrained ResNet50:
  ```python
  base_model = ResNet50(
      weights='imagenet',
      include_top=False,
      input_shape=(224, 224, 3)
  )
  ```
- [ ] Freeze base layers (first 140 layers)
- [ ] Add custom top:
  ```python
  GlobalAveragePooling2D()
  Dense(1024, activation='relu')
  Dropout(0.5)
  Dense(2, activation='sigmoid')
  ```

### Ngày 3-4 (06-08/12): Fine-tuning & Training

- [ ] Phase 1: Train top layers only
  - Epochs: 10
  - Learning rate: 0.001

- [ ] Phase 2: Unfreeze & fine-tune
  - Unfreeze last 50 layers
  - Epochs: 20
  - Learning rate: 0.0001

- [ ] Evaluate:
  - Test accuracy > 92%
  - Confusion matrix
  - Compare với CNN (Quốc Anh)

### Ngày 5 (09/12): Save & Download

- [ ] Save model: `resnet50_best.h5`
- [ ] Download về `models/resnet50_best.h5`
- [ ] Commit model lên GitHub (Git LFS)
- [ ] Write training notes

---

## PART 2: Flask Service Setup (2 ngày) - OPTIONAL

### Ngày 6-7 (10-11/12): Model Service

- [ ] Setup Flask project:
  ```
  model-service/
  ├── app/
  │   ├── routes/
  │   ├── services/
  │   └── utils/
  ├── requirements.txt
  └── Dockerfile
  ```

- [ ] Load models:
  ```python
  cnn_model = load_model('models/cnn_best.h5')
  resnet_model = load_model('models/resnet50_best.h5')
  ```

- [ ] Create endpoints:
  - `POST /predict/cnn`
  - `POST /predict/resnet50`
  - `GET /health`

- [ ] Test với Postman
- [ ] **Demo ResNet model cho team**

---

## Output Deliverables

- `models/resnet50_best.h5` - Trained ResNet50 model
- Flask service (nếu làm)
- Training comparison notes

---

## Expected Metrics

- Training accuracy: ~94-96%
- Validation accuracy: ~92-94%
- Test accuracy: ~92-96%

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 3 - Full Integration & Comparison
