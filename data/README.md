# Data Directory

**Owner:** Quang Duy | **Deadline:** 04/12/2025

## Download Dataset

**Nguồn:** [Kaggle - Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

```bash
# Download và giải nén vào data/raw/
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
```

## Preprocessing Scripts

Chạy theo thứ tự trong `preprocessing-scripts/`:

1. `01_data_inspection.py` - Kiểm tra dataset
2. `02_data_cleaning.py` - Loại bỏ ảnh lỗi
3. `03_preprocessing.py` - Resize 224x224, normalize
4. `04_augmentation.py` - Tăng cường dữ liệu
5. `05_split_dataset.py` - Chia train/val/test

## Output

- Dataset đã xử lý: `processed/train/`, `val/`, `test/`
- Báo cáo: `reports/preprocessing_report.md`

**Lưu ý:** KHÔNG commit thư mục `raw/` và `processed/` (quá lớn)
