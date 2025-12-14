"""
Grad-CAM Visualization Page
"""
import streamlit as st
from PIL import Image
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from utils.visualization import generate_gradcam_heatmap, overlay_heatmap_on_image
    from utils.ui_components import show_info_box
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

st.set_page_config(
    page_title="Grad-CAM Visualization | HCMUTE",
    layout="wide"
)

st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #0066CC 0%, #003d82 100%); 
            color: white; border-radius: 12px; margin-bottom: 2rem;">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Grad-CAM Visualization</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Hiển thị vùng tập trung của model</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Grad-CAM** (Gradient-weighted Class Activation Mapping) giúp visualize vùng mà model đang chú ý khi đưa ra dự đoán.

- **Vùng đỏ/cam:** Model chú ý nhiều (quan trọng cho quyết định)
- **Vùng xanh:** Model chú ý ít
""")

# Check if models are loaded
if 'cnn_model' not in st.session_state:
    st.warning("⚠️ CNN model chưa được load. Vui lòng quay lại trang chính để load models.")
    st.info("💡 **Hướng dẫn:** Truy cập trang chính (Home) để load models, sau đó quay lại đây.")
    st.stop()

# Model selection - chỉ hiển thị models đã được load
available_models = []
if st.session_state.get('cnn_model') is not None:
    available_models.append("CNN")
if st.session_state.get('resnet_model') is not None:
    available_models.append("ResNet-50")

if not available_models:
    st.error("Không có model nào được load!")
    st.stop()

model_choice = st.radio(
    "Chọn model để visualize:",
    available_models,
    horizontal=True
)

# File upload
uploaded_file = st.file_uploader(
    "Upload ảnh X-quang",
    type=['jpg', 'jpeg', 'png'],
    help="Upload ảnh để xem Grad-CAM visualization"
)

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)
    
    # Initialize heatmap variable in outer scope
    heatmap = None
    
    with col2:
        st.subheader("Grad-CAM Heatmap")
        
        if UTILS_AVAILABLE:
            with st.spinner("Generating Grad-CAM..."):
                try:
                    # Select model
                    model = st.session_state.cnn_model if model_choice == "CNN" else st.session_state.resnet_model
                    
                    # Preprocess image (same as main app)
                    if model_choice == "CNN":
                        # CNN: 144x144 grayscale
                        img_resized = image.convert('L').resize((144, 144))
                        img_array = np.array(img_resized) / 255.0
                        img_array = np.expand_dims(np.expand_dims(img_array, 0), -1)
                    else:
                        # ResNet: 224x224 RGB
                        img_resized = image.convert('RGB').resize((224, 224))
                        img_array = np.array(img_resized) / 255.0
                        img_array = np.expand_dims(img_array, axis=0)
                    
                    # Build model by calling it once
                    _ = model.predict(img_array, verbose=0)
                    
                    # Generate heatmap
                    heatmap = generate_gradcam_heatmap(model, img_array)
                    
                    # Display heatmap
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()
                    ax.imshow(heatmap, cmap='jet')
                    ax.axis('off')
                    st.pyplot(fig)
                    
                except Exception as e:
                    st.error(f"Error generating Grad-CAM: {e}")
        else:
            st.warning("Visualization utilities not available")
    
    with col3:
        st.subheader("Overlay")
        
        if UTILS_AVAILABLE and heatmap is not None:
            try:
                # Create overlay
                overlay_img = overlay_heatmap_on_image(image, heatmap, alpha=0.4)
                st.image(overlay_img, use_container_width=True)
                
                st.success("Grad-CAM visualization completed!")
                
            except Exception as e:
                st.error(f"Error creating overlay: {e}")
        else:
            st.info("Heatmap chưa được generate hoặc có lỗi ở bước trước")
    
    # Interpretation guide
    st.markdown("---")
    st.subheader("How to Interpret Grad-CAM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Red/Orange areas:**
        - High activation regions
        - Model focuses here for prediction
        - Important features detected
        
        **Blue areas:**
        - Low activation
        - Less relevant for decision
        """)
    
    with col2:
        st.markdown("""
        **For Pneumonia Detection:**
        - Model should focus on lung regions
        - Abnormal patterns (infiltrates, consolidation)
        - Not focused on edges or irrelevant areas
        
        **Good Grad-CAM:**
        - Highlights actual pneumonia patterns
        - Focused on relevant anatomical regions
        """)

else:
    st.info("Upload ảnh X-quang để xem Grad-CAM visualization")
    
    # Example explanation
    st.markdown("---")
    st.subheader("About Grad-CAM")
    
    st.markdown("""
    ### Grad-CAM hoạt động như thế nào?
    
    1. **Forward pass:** Input ảnh qua model
    2. **Backward pass:** Tính gradient của output class wrt. feature maps
    3. **Weighted sum:** Kết hợp feature maps với gradients
    4. **Normalization:** Chuẩn hóa về [0, 1] và tạo heatmap
    
    ### Lợi ích:
    
    <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <ul style="line-height: 1.8; color: #444;">
            <li>Giải thích được quyết định của model</li>
            <li>Phát hiện nếu model học sai</li>
            <li>Tăng độ tin cậy cho predictions</li>
            <li>Debug model performance</li>
        </ul>
    </div>
    """)

# Footer
st.markdown("---")
st.caption("Grad-CAM helps understand which regions of the X-ray image influenced the model's decision.")
