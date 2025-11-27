# Streamlit App

**Tech Stack:** Python + Streamlit + TensorFlow

## Setup môi trường

```bash
cd app

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài packages
pip install -r requirements.txt
```

## Chạy app

### Cách 1: Sử dụng script (Khuyến nghị cho macOS)

```bash
./run.sh
```

### Cách 2: Manual

```bash
# macOS
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
source venv/bin/activate
streamlit run app.py

# Windows
venv\Scripts\activate
streamlit run app.py

# Linux
source venv/bin/activate
streamlit run app.py
```

App sẽ mở tại: **http://localhost:8501**

### Troubleshooting macOS Crash

Nếu app crash với lỗi `mutex lock failed`:

1. **Đã fix:** File `.streamlit/config.toml` và script `run.sh` đã được cấu hình sẵn
2. **Chạy bằng:** `./run.sh` thay vì `streamlit run app.py`
3. **Nguyên nhân:** Conflict giữa TensorFlow + Streamlit threading trên macOS
4. **Giải pháp:** Biến môi trường `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

## Cấu trúc

```
app/
├── app.py                    # Main Streamlit application (Home page)
├── pages/                    # Multi-page app pages
│   ├── 1_Model_Performance.py     # Training metrics & comparison
│   ├── 2_Grad-CAM_Visualization.py # Heatmap visualization
│   └── 3_Image_Enhancement.py     # Preprocessing tools
├── utils/                    # Helper functions
│   ├── __init__.py
│   ├── ui_components.py      # UI components & CSS loader
│   ├── visualization.py      # Grad-CAM, charts, metrics
│   └── image_processing.py   # Image enhancement utilities
├── static/                   # Static assets
│   ├── styles.css           # Custom CSS styling
│   ├── CSS_GUIDE.md         # CSS customization guide
│   └── images/              # Logo, icons (optional)
├── requirements.txt          # Python dependencies
├── MULTIPAGE_GUIDE.md       # Multi-page app guide
└── README.md
```

## Custom CSS

App hỗ trợ 2 cách styling:

1. **External CSS** (recommended): File `static/styles.css` được load tự động
2. **Fallback**: Inline CSS nếu không tìm thấy file

Xem `static/CSS_GUIDE.md` để biết cách customize thêm.

## Features

### Main Page (app.py)
- Upload ảnh X-quang
- Chọn model (CNN / ResNet-50)
- Predict với confidence score
- Custom CSS styling

### Model Performance
- Training history charts (accuracy, loss)
- Metrics comparison table
- Confusion matrices
- Side-by-side model comparison

### Grad-CAM Visualization
- Heatmap visualization
- Vùng model chú ý khi predict
- Overlay heatmap trên ảnh gốc
- Giải thích model decisions

### Image Enhancement
- Brightness/Contrast adjustment
- CLAHE (recommended for X-rays)
- Denoising
- Sharpness enhancement
- Download enhanced images

## Multi-Page Navigation

Streamlit tự động tạo sidebar với navigation:
- Home (app.py)
- Model Performance
- Grad-CAM Visualization
- Image Enhancement

Xem `MULTIPAGE_GUIDE.md` để hiểu cách hoạt động.

## Features

- Upload ảnh X-quang
- Chọn model: CNN hoặc ResNet-50
- Hiển thị kết quả: Normal/Pneumonia
- Confidence score
- Responsive UI

## Structure

```
app/
├── app.py              # Main Streamlit app
├── utils/              # Helper functions (nếu cần)
├── requirements.txt    # Python dependencies
└── README.md
```

## Lưu ý

- Models phải được train trước (xem `notebooks/`)
- Models lưu tại `models/cnn_best.h5` và `models/resnet50_best.h5`
- App chỉ chạy inference (predict), không train
