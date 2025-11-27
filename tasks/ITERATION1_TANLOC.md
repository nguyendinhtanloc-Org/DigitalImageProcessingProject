# Iteration 1 - Tấn Lộc (27/11 - 04/12)

**Mục tiêu:** Chuẩn bị ResNet Notebook

---

## Checklist

### Ngày 1-3 (27-29/11): Research & Setup

- [ ] Đọc về ResNet-50 architecture
- [ ] Research Transfer Learning
- [ ] Tạo notebook template `notebooks/ResNet.ipynb`
- [ ] Setup Kaggle account

### Ngày 4-7 (30/11-04/12): Notebook Development

- [ ] Viết code load pretrained ResNet50:
  ```python
  from tensorflow.keras.applications import ResNet50
  base_model = ResNet50(weights='imagenet', include_top=False)
  ```

- [ ] Freeze base layers
- [ ] Add custom top layers
- [ ] Code fine-tuning strategy
- [ ] Code training loop
- [ ] Code evaluation

- [ ] Test notebook locally (với subset nhỏ)
- [ ] Commit notebook lên GitHub

---

## Output

- `notebooks/ResNet.ipynb` - Notebook ready để upload Kaggle

---

**Next:** Iteration 2 - Train ResNet50 trên Kaggle
