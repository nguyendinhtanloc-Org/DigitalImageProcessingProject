# Iteration 1 - Quang Duy (27/11 - 04/12)

**Mục tiêu:** Hoàn thành data preprocessing

---

## Checklist

### Ngày 1-2 (27-28/11): Download & Inspection

- [ ] Setup môi trường Python
  ```bash
  cd data
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  # venv\Scripts\activate   # Windows
  pip install -r requirements.txt
  ```

- [ ] Download dataset từ Kaggle
  ```bash
  kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
  ```
- [ ] Giải nén vào `data/raw/`
- [ ] Chạy `01_data_inspection.py`
- [ ] Viết báo cáo: `data/reports/data_inspection_report.md`
  - Số lượng ảnh mỗi class
  - Image size, format
  - Ảnh bị lỗi/thiếu

### Ngày 3-4 (29-30/11): Cleaning & Preprocessing

- [ ] Chạy `02_data_cleaning.py`
  - Loại bỏ ảnh lỗi, trùng, sai format
- [ ] Chạy `03_preprocessing.py`
  - Resize: 224x224
  - Normalize: [0, 1]
  - Convert grayscale → RGB

### Ngày 5-6 (01-02/12): Augmentation & Split

- [ ] Chạy `04_augmentation.py`
  - Rotation, flip, zoom, brightness
  - Cân bằng class (PNEUMONIA nhiều hơn NORMAL)
- [ ] Chạy `05_split_dataset.py`
  - Train: 80%, Val: 10%, Test: 10%
  - Output: `data/processed/`

### Ngày 7 (03-04/12): Verification & Handoff

- [ ] Verify dataset cuối cùng
  - Check số lượng ảnh từng folder
  - Test load vài ảnh random
- [ ] Viết báo cáo: `data/reports/preprocessing_report.md`
- [ ] Commit code lên GitHub
- [ ] **Bàn giao dataset cho Quốc Anh & Tấn Lộc**

---

## Output Deliverables

- `data/processed/train/` - Dataset training
- `data/processed/val/` - Dataset validation  
- `data/processed/test/` - Dataset testing
- `data/reports/preprocessing_report.md` - Báo cáo chi tiết

---

## Notes

- Dataset raw KHÔNG commit (thêm vào `.gitignore`)
- Chỉ commit scripts và reports
- Chia sẻ processed data qua Google Drive nếu cần

---

**Status:** TODO → DOING → DONE ✓  
**Next:** Iteration 2 - Backend API
