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
                    
                    # Generate heatmap (model will be built inside this function)
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
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h2 style="margin: 0 0 1rem 0; font-size: 1.8rem;">🔍 Hướng dẫn hiểu Grad-CAM Heatmap</h2>
        <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;">
            Grad-CAM (Gradient-weighted Class Activation Mapping) giúp bạn <strong>nhìn thấy model đang "nhìn" vào đâu</strong> khi đưa ra dự đoán.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Ý nghĩa màu sắc trong Heatmap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #FF9800;">
            <h4 style="color: #E65100; margin-top: 0;">🔴 Vùng ĐỎ/CAM/VÀNG (Hot zones)</h4>
            <ul style="line-height: 1.8; color: #444;">
                <li><strong>Activation cao:</strong> Model chú ý NHIỀU nhất</li>
                <li><strong>Quan trọng:</strong> Đây là vùng quyết định prediction</li>
                <li><strong>Với Pneumonia:</strong> Thường ở lung regions có tổn thương</li>
                <li><strong>Giá trị:</strong> Gần 1.0 (100% attention)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #E8F5E9; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #4CAF50; margin-top: 1rem;">
            <h4 style="color: #1B5E20; margin-top: 0;">🟢 Vùng XANH LÁ (Medium zones)</h4>
            <ul style="line-height: 1.8; color: #444;">
                <li><strong>Activation trung bình:</strong> Model có chú ý nhưng không ưu tiên</li>
                <li><strong>Giá trị:</strong> 0.3 - 0.7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #E3F2FD; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #2196F3;">
            <h4 style="color: #0D47A1; margin-top: 0;">🔵 Vùng XANH DƯƠNG (Cold zones)</h4>
            <ul style="line-height: 1.8; color: #444;">
                <li><strong>Activation thấp:</strong> Model GẦN NHƯ BỎ QUA</li>
                <li><strong>Không quan trọng:</strong> Không ảnh hưởng quyết định</li>
                <li><strong>Ví dụ:</strong> Background, viền ảnh, vùng không liên quan</li>
                <li><strong>Giá trị:</strong> Gần 0.0 (0% attention)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏥 Cách đọc kết quả cho Pneumonia Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Dấu hiệu GOOD (Model học đúng)
        
        <div style="background: #F1F8E9; padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
            <p style="margin: 0; line-height: 1.8; color: #444;">
                ✓ <strong>Focus vào lung regions</strong> (2 phổi)<br>
                ✓ <strong>Highlight vùng có infiltrates</strong> (đám mờ)<br>
                ✓ <strong>Tập trung vào abnormal patterns</strong><br>
                ✓ <strong>Bỏ qua background</strong> và edges<br>
                ✓ <strong>Symmetric attention</strong> cho cả 2 phổi (nếu cần)
            </p>
        </div>
        
        **Ví dụ trong ảnh của bạn:**
        - Vùng vàng/đỏ xuất hiện ở **giữa ảnh** → có thể là lung region
        - Model đang chú ý vào **các vùng có texture khác biệt**
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ Dấu hiệu BAD (Model học sai)
        
        <div style="background: #FFEBEE; padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
            <p style="margin: 0; line-height: 1.8; color: #444;">
                ✗ <strong>Focus vào text/labels</strong> trên ảnh<br>
                ✗ <strong>Chú ý vào viền/góc ảnh</strong><br>
                ✗ <strong>Highlight vùng không liên quan</strong> (ngoài phổi)<br>
                ✗ <strong>Attention lan tỏa</strong> không rõ ràng<br>
                ✗ <strong>Bỏ qua lung regions</strong> hoàn toàn
            </p>
        </div>
        
        **Cách khắc phục:**
        - Retrain model với data augmentation tốt hơn
        - Loại bỏ text/artifacts khỏi training images
        - Sử dụng attention mechanisms trong architecture
        """)
    
    st.markdown("---")
    st.subheader("🔬 Giải thích kỹ thuật")
    
    with st.expander("📖 Grad-CAM hoạt động như thế nào?"):
        st.markdown("""
        ### Các bước tính toán:
        
        1. **Forward pass:** Đưa ảnh qua model CNN
        2. **Lấy feature maps:** Từ last convolutional layer (18×18×256)
        3. **Backward pass:** Tính gradient của predicted class wrt. feature maps
        4. **Global Average Pooling:** Tính trung bình gradients → weights cho mỗi channel
        5. **Weighted combination:** Nhân weights với feature maps và cộng lại
        6. **ReLU + Normalize:** Loại bỏ giá trị âm và chuẩn hóa về [0, 1]
        7. **Upsampling:** Resize 18×18 → kích thước ảnh gốc
        
        ### Công thức toán học:
        
        ```
        L_Grad-CAM = ReLU(Σ(αk * Ak))
        
        Trong đó:
        - αk = (1/Z) * Σ Σ (∂yc/∂Akij)  (global average pooling of gradients)
        - Ak = feature map thứ k từ last conv layer
        - yc = score của class c (predicted class)
        ```
        
        ### Tại sao heatmap có độ phân giải thấp (18×18)?
        
        - Last Conv2D layer của model có output shape: **18×18×256**
        - Input: 144×144 → qua 4 MaxPooling (÷2 mỗi lần) → 144÷8 = 18
        - Sau đó được **resize lên** kích thước ảnh gốc để overlay
        - Pixelation là bình thường - cho thấy "field of view" của conv layers
        """)
    
    with st.expander("💡 Tại sao cần Grad-CAM?"):
        st.markdown("""
        ### Lợi ích trong thực tế:
        
        1. **Explainability (Giải thích được):**
           - Bác sĩ/người dùng hiểu tại sao model đưa ra kết luận
           - Tăng độ tin cậy khi deploy vào môi trường y tế
        
        2. **Debugging (Phát hiện lỗi):**
           - Phát hiện model học sai (focus vào text, artifacts)
           - Validate model học đúng features (lung patterns)
        
        3. **Model improvement:**
           - Hiểu model đang "nhìn" gì
           - Cải thiện data quality/augmentation
        
        4. **Trust & Compliance:**
           - FDA/regulatory bodies yêu cầu explainability cho AI y tế
           - Tránh "black box" models
        
        ### So với các phương pháp khác:
        
        | Method | Pros | Cons |
        |--------|------|------|
        | **Grad-CAM** | ✓ Class-specific<br>✓ Dễ hiểu<br>✓ Resolution vừa phải | ✗ Coarse localization |
        | LIME | ✓ Model-agnostic | ✗ Slow, không class-specific |
        | Attention Maps | ✓ High resolution | ✗ Cần architecture change |
        | Saliency Maps | ✓ Pixel-level | ✗ Noisy, khó interpret |
        """)

else:
    st.info("📤 Upload ảnh X-quang để xem Grad-CAM visualization")
    
    # Example explanation
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h2 style="margin: 0 0 1rem 0; font-size: 1.8rem;">🔍 Grad-CAM là gì?</h2>
        <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;">
            <strong>Gradient-weighted Class Activation Mapping</strong> - Công cụ visualization giúp hiểu model CNN đang "nhìn" vào đâu khi dự đoán.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
