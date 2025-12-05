import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Disable TensorFlow for now (enable after models are trained)
ENABLE_TENSORFLOW = False

if ENABLE_TENSORFLOW:
    try:
        import tensorflow as tf
        from tensorflow import keras
        TF_AVAILABLE = True
    except Exception as e:
        st.warning(f"TensorFlow import failed: {e}")
        TF_AVAILABLE = False
else:
    TF_AVAILABLE = False

# Import custom UI components
try:
    from utils.ui_components import (
        load_css, 
        render_header, 
        render_prediction_card, 
        render_footer,
        show_info_box
    )
    USE_CUSTOM_UI = True
except ImportError:
    USE_CUSTOM_UI = False

# Page config
st.set_page_config(
    page_title="Pneumonia Detection | HCMUTE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS if available
if USE_CUSTOM_UI:
    load_css()
else:
    # Fallback inline CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1F77B4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .prediction-box {
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 1rem 0;
        }
        .normal {
            background-color: #d4edda;
            color: #155724;
            border: 2px solid #28a745;
        }
        .pneumonia {
            background-color: #f8d7da;
            color: #721c24;
            border: 2px solid #dc3545;
        }
    </style>
    """, unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    """Load trained models"""
    if not TF_AVAILABLE:
        return None, None
    
    try:
        cnn_model = keras.models.load_model('../models/cnn_best.h5')
        resnet_model = keras.models.load_model('../models/resnet50_best.h5')
        return cnn_model, resnet_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(image)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict(model, image_array):
    """Make prediction"""
    prediction = model.predict(image_array, verbose=0)
    confidence = float(prediction[0][0])
    
    # Assuming binary classification: 0 = Normal, 1 = Pneumonia
    if confidence > 0.5:
        label = "PNEUMONIA"
        conf_percentage = confidence * 100
    else:
        label = "NORMAL"
        conf_percentage = (1 - confidence) * 100
    
    return label, conf_percentage

# Main UI - Header
if USE_CUSTOM_UI:
    render_header()
else:
    st.markdown('<h1 class="main-header">Pneumonia Detection from Chest X-Ray</h1>', unsafe_allow_html=True)

st.markdown("""
### Dự án phân loại ảnh X-quang phổi sử dụng Deep Learning
**Mục tiêu:** Phát hiện viêm phổi (Pneumonia) từ ảnh X-quang ngực

**Models:** Custom CNN & ResNet-50 Transfer Learning
""")

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #0066CC; margin-bottom: 0.5rem;">Cấu hình</h2>
        <p style="color: #666; font-size: 0.9rem;">Model & Settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    model_choice = st.radio(
        "Chọn model:",
        ["CNN", "ResNet-50"],
        help="CNN: Custom architecture | ResNet-50: Transfer Learning"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 0.5rem;">
        <h3 style="color: #0066CC; font-size: 1.1rem; margin-bottom: 1rem;">Hướng dẫn sử dụng</h3>
        <ol style="font-size: 0.9rem; line-height: 1.8; color: #444;">
            <li>Chọn model (CNN hoặc ResNet-50)</li>
            <li>Upload ảnh X-quang ngực</li>
            <li>Xem kết quả phân tích</li>
        </ol>
        
        <h3 style="color: #0066CC; font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 1rem;">Team Prompt Engineer</h3>
        <p style="font-size: 0.85rem; line-height: 1.6; color: #666;">
            Nguyễn Văn Quang Duy<br>
            Nguyễn Đặng Quốc Anh<br>
            Nguyễn Đình Tấn Lộc
        </p>
    </div>
    """, unsafe_allow_html=True)

# Load models
cnn_model, resnet_model = load_models()

if not TF_AVAILABLE:
    st.warning("**Demo Mode:** TensorFlow disabled for testing. Enable in code after training models.")
    st.info("""
    **Hướng dẫn kích hoạt dự đoán:**
    1. Train models trên Kaggle (CNN.ipynb & ResNet.ipynb)
    2. Download `cnn_best.h5` & `resnet50_best.h5` 
    3. Đặt vào thư mục `models/`
    4. Set `ENABLE_TENSORFLOW = True` trong app.py (line 7)
    """)
    models_ready = False
elif cnn_model is None or resnet_model is None:
    if USE_CUSTOM_UI:
        show_info_box("Models chưa được train! Vui lòng train models trước.", type="error")
        show_info_box("Hướng dẫn: Chạy notebooks/CNN.ipynb và notebooks/ResNet.ipynb trên Kaggle để train models.", type="info")
    else:
        st.error("Models chưa được train! Vui lòng train models trước.")
        st.info("Hướng dẫn: Chạy notebooks/CNN.ipynb và notebooks/ResNet.ipynb trên Kaggle để train models.")
    models_ready = False
else:
    models_ready = True

# File uploader
st.markdown("""
<div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
            padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; border-left: 4px solid #0066CC;">
    <h3 style="color: #0066CC; margin: 0 0 0.5rem 0;">Upload ảnh X-quang</h3>
    <p style="color: #666; margin: 0; font-size: 0.9rem;">Hỗ trợ định dạng JPG, PNG</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Chọn file ảnh",
    type=['jpg', 'jpeg', 'png'],
    help="Chọn ảnh X-quang định dạng JPG hoặc PNG",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Display image
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3 style="color: #0066CC; font-weight: 600;">Ảnh gốc</h3>
        </div>
        """, unsafe_allow_html=True)
        
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        # Image info
        st.markdown(f"""
        <div style="background: #F8F9FA; padding: 0.75rem; border-radius: 8px; margin-top: 1rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem; text-align: center;">
                <strong>Size:</strong> {image.size[0]}×{image.size[1]} | 
                <strong>Format:</strong> {image.format}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3 style="color: #0066CC; font-weight: 600;">Kết quả phân tích</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if not models_ready:
            st.info("Predictions disabled - models not available")
            st.write("**Demo Mode:** Upload working, but predictions require trained models.")
        else:
            # Preprocess
            with st.spinner("Đang xử lý ảnh..."):
                processed_image = preprocess_image(image)
            
            # Select model
            selected_model = cnn_model if model_choice == "CNN" else resnet_model
            
            # Predict
            with st.spinner(f"Đang dự đoán với {model_choice}..."):
                label, confidence = predict(selected_model, processed_image)
        
            # Display result with custom component if available
            if USE_CUSTOM_UI:
                model_display_name = f"{model_choice} Model"
                render_prediction_card(label, confidence, model_display_name)
            else:
                css_class = "normal" if label == "NORMAL" else "pneumonia"
                st.markdown(
                    f'<div class="prediction-box {css_class}">{label}</div>',
                    unsafe_allow_html=True
                )
            
            # Confidence metric
            st.markdown("""
            <div style="background: linear-gradient(135deg, #F8F9FA 0%, #E8EEF3 100%); 
                        padding: 1.2rem; border-radius: 12px; margin: 1rem 0; text-align: center;">
                <p style="color: #666; margin: 0 0 0.5rem 0; font-size: 0.9rem; font-weight: 500;">Độ tin cậy</p>
                <p style="color: #0066CC; margin: 0; font-size: 2rem; font-weight: 700;">{:.1f}%</p>
            </div>
            """.format(confidence), unsafe_allow_html=True)
            
            # Progress bar
            st.progress(int(confidence) / 100)
            
            # Model info
            st.markdown(f"""
            <div style="background: #E8F5E9; padding: 0.75rem; border-radius: 8px; margin: 1rem 0; border-left: 3px solid #00C853;">
                <p style="margin: 0; color: #2E7D32; font-weight: 500;">Model: <strong>{model_choice}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional info
            if label == "PNEUMONIA":
                st.markdown("""
                <div style="background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); 
                            padding: 1rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #D32F2F;">
                    <p style="margin: 0; color: #C62828; font-weight: 600;">Cảnh báo</p>
                    <p style="margin: 0.5rem 0 0 0; color: #B71C1C;">Phát hiện dấu hiệu viêm phổi. Vui lòng tham khảo ý kiến bác sĩ.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                            padding: 1rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #00C853;">
                    <p style="margin: 0; color: #2E7D32; font-weight: 600;">Kết quả</p>
                    <p style="margin: 0.5rem 0 0 0; color: #1B5E20;">Không phát hiện dấu hiệu bất thường.</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")

if USE_CUSTOM_UI:
    render_footer()
else:
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p style="margin: 0 0 0.5rem 0; font-weight: 500;">Đồ án Xử Lý Ảnh Số - Năm học 2024-2025</p>
        <p style="margin: 0; font-size: 0.85rem; color: #999;">Chỉ dùng cho mục đích học tập - Không thay thế chẩn đoán y khoa</p>
    </div>
    """, unsafe_allow_html=True)
