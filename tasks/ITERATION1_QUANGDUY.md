# Iteration 1 - Quang Duy (27/11 - 04/12)

**Mục tiêu:** Data Preprocessing

---

## Checklist

### Ngày 1-2 (27-28/11): Setup & Download

- [ ] Setup môi trường Python
  ```bash
  cd data
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- [ ] Download dataset từ Kaggle
  ```bash
  kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
  ```

- [ ] Giải nén vào `data/raw/`
- [ ] Chạy `01_data_inspection.py`
- [ ] Viết báo cáo inspection

### Ngày 3-4 (29-30/11): Cleaning & Preprocessing

- [ ] Chạy `02_data_cleaning.py`
  - Loại bỏ ảnh lỗi, trùng

- [ ] Chạy `03_preprocessing.py`
  - Resize: 224x224
  - Normalize: [0, 1]
  - Convert grayscale → RGB

### Ngày 5-6 (01-02/12): Augmentation & Split

- [ ] Chạy `04_augmentation.py`
  - Rotation, flip, zoom, brightness

- [ ] Chạy `05_split_dataset.py`
  - Train: 80%, Val: 10%, Test: 10%

### Ngày 7 (03-04/12): Verification

- [ ] Verify dataset
- [ ] Viết báo cáo preprocessing
- [ ] Commit code
- [ ] Bàn giao dataset cho Quốc Anh & Tấn Lộc

---

## Output

- `data/processed/train/`, `val/`, `test/`
- `data/reports/preprocessing_report.md`

---

**Next:** Iteration 2 - Setup Streamlit app
