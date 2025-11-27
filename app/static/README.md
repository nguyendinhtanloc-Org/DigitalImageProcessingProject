# Static Assets

Thư mục này chứa các file tĩnh cho Streamlit app:

## Cấu trúc

```
static/
├── styles.css          # Custom CSS styling
├── images/             # Logo, icons (nếu có)
└── README.md
```

## CSS Customization

File `styles.css` chứa custom styling cho:
- Layout chính
- Sidebar
- Prediction cards (Normal/Pneumonia themes)
- Buttons, progress bars
- Responsive design

## Cách sử dụng

CSS được load tự động trong `app.py` thông qua hàm `load_css()` từ `utils/ui_components.py`:

```python
from utils.ui_components import load_css

load_css()
```

## Thêm images/icons

Nếu muốn thêm logo hoặc icons:

1. Tạo thư mục `images/`:
```bash
mkdir -p static/images
```

2. Copy files vào `static/images/`

3. Load trong app:
```python
from PIL import Image

logo = Image.open("static/images/logo.png")
st.image(logo, width=200)
```
