# Streamlit Multi-Page App Structure

Streamlit tự động phát hiện multi-page apps dựa trên cấu trúc thư mục.

## Cấu trúc

```
app/
├── app.py                          # Main page (Home)
├── pages/                          # Additional pages
│   ├── 1_Model_Performance.py      # Auto-detected as page 1
│   ├── 2_Grad-CAM_Visualization.py
│   └── 3_Image_Enhancement.py
├── utils/
├── static/
└── requirements.txt
```

## Quy tắc đặt tên

- Files trong `pages/` tự động trở thành pages
- Format: `[number]_[Name].py`
- Number để sắp xếp thứ tự
- Name là title của page

## Navigation

Streamlit tự động tạo sidebar navigation với:
- Icon từ filename emoji
- Title từ filename

## Session State

Share data giữa pages qua `st.session_state`:

```python
# In main app.py
st.session_state.cnn_model = cnn_model

# In pages/1_...py
model = st.session_state.cnn_model
```

## Best Practices

1. **Main app.py**: Upload, predict, core features
2. **Pages**: Specialized features (analytics, visualization)
3. **Utils**: Shared functions
4. **Static**: CSS, images

## Example Flow

```
Home (app.py)
  ↓
User uploads image → Predict
  ↓
Navigate to Grad-CAM page → See visualization
  ↓
Navigate to Performance page → Compare models
```
