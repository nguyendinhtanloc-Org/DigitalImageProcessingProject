# Iteration 2 - Quang Duy (04/12 - 11/12)

**Mục tiêu:** Setup Streamlit Multi-Page App với Advanced Features

---

## Tasks Overview

### Task 1: Multi-Page App Structure (Day 1-2)
### Task 2: CSS & UI Components (Day 2-3)
### Task 3: Model Performance Dashboard (Day 4-5)
### Task 4: Grad-CAM Visualization (Day 5-6)
### Task 5: Image Enhancement Tools (Day 6-7)
### Task 6: Documentation & Testing (Day 7)

---

## Task 1: Multi-Page App Structure

**Setup môi trường và cấu trúc app**

Steps:
1. Setup Python environment:
```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Tạo cấu trúc multi-page:
```
app/
├── app.py                    # Main page
├── pages/
│   ├── 1_Model_Performance.py
│   ├── 2_Grad-CAM_Visualization.py
│   └── 3_Image_Enhancement.py
├── utils/
│   ├── __init__.py
│   ├── ui_components.py
│   ├── visualization.py
│   └── image_processing.py
└── static/
    └── styles.css
```

3. Test navigation:
```bash
streamlit run app.py
# Check sidebar shows all pages
```

Deliverables:
- [ ] Folder structure complete
- [ ] All pages accessible
- [ ] Navigation working

---

## Task 2: CSS & UI Components

**Tạo custom styling và reusable components**

Implement:
1. `static/styles.css`:
   - Main layout
   - Prediction cards (green/red)
   - Responsive design
   - Buttons, progress bars

2. `utils/ui_components.py`:
   - `load_css()` - Load external CSS
   - `render_header()` - App header
   - `render_prediction_card()` - Results display
   - `render_footer()` - Footer
   - `show_info_box()` - Info/warning boxes

3. Update `app.py` to use components

Testing:
```bash
streamlit run app.py
# Check CSS loaded
# Test UI components render
```

Deliverables:
- [ ] External CSS working
- [ ] UI components functional
- [ ] Clean, professional UI

---

## Task 3: Model Performance Dashboard

**Tạo dashboard so sánh models**

Implement `pages/1_Model_Performance.py`:
- 3 tabs: Training History, Metrics, Confusion Matrix
- Training curves (accuracy/loss)
- Comparison table (CNN vs ResNet)
- Metrics cards (Accuracy, Precision, Recall, F1)

Implement `utils/visualization.py`:
- `plot_training_history()` - Charts
- `create_comparison_table()` - HTML table
- `create_metrics_cards()` - Metrics display

Use mock data initially

Deliverables:
- [ ] Performance dashboard complete
- [ ] All charts working
- [ ] Comparison table functional

---

## Task 4: Grad-CAM Visualization

**Visualize vùng model chú ý**

Implement `pages/2_Grad-CAM_Visualization.py`:
- Upload image interface
- Generate heatmap
- 3-column layout: Original, Heatmap, Overlay
- Interpretation guide

Implement trong `utils/visualization.py`:
- `generate_gradcam_heatmap()` - Create heatmap
- `overlay_heatmap_on_image()` - Overlay viz

Features:
- Auto-detect last conv layer
- Red = high attention areas
- Support CNN & ResNet-50

Deliverables:
- [ ] Grad-CAM page working
- [ ] Heatmap generation functional
- [ ] Overlay working

---

## Task 5: Image Enhancement Tools

**Preprocessing tools cho X-ray images**

Implement `pages/3_Image_Enhancement.py`:
- Brightness/Contrast sliders
- CLAHE checkbox (recommended for X-rays)
- Denoising with strength control
- Sharpness adjustment
- Before/After comparison
- Download button

Implement `utils/image_processing.py`:
- `adjust_brightness/contrast/sharpness()`
- `apply_clahe()` - X-ray enhancement
- `denoise_image()` - Noise removal
- `preprocess_xray()` - Complete pipeline

Deliverables:
- [ ] Enhancement page complete
- [ ] All filters working
- [ ] Download function works

---

## Task 6: Documentation & Testing

**Hoàn thiện docs và testing**

Documentation:
1. Update `app/README.md`:
   - Multi-page structure
   - Features list
   - Setup guide

2. Create `app/MULTIPAGE_GUIDE.md`:
   - How multi-page works
   - Navigation structure

3. Create `app/static/CSS_GUIDE.md`:
   - CSS customization guide

Testing:
- [ ] Test all pages
- [ ] Test navigation
- [ ] Test with/without models
- [ ] Responsive design check
- [ ] Browser compatibility

Deliverables:
- [ ] Complete documentation
- [ ] All features tested
- [ ] README updated

---

## Final Checklist

- [ ] Multi-page app structure
- [ ] Custom CSS & UI components
- [ ] Model Performance dashboard
- [ ] Grad-CAM visualization
- [ ] Image Enhancement tools
- [ ] Complete documentation
- [ ] All features tested

---

**Next:** Iteration 3 - Deployment & Final Polish
