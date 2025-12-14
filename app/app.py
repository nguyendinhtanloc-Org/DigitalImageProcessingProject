import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Enable TensorFlow now that CNN model is available
ENABLE_TENSORFLOW = True

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
        # Load CNN model (TensorFlow/Keras format)
        cnn_model = keras.models.load_model('../models/cnn_pneumonia_model.keras')
        
        # ResNet model not available yet (PyTorch format in notebook)
        resnet_model = None
        
        return cnn_model, resnet_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

def preprocess_image(image, target_size=144):
    """Preprocess image for model prediction (simple version without steps)"""
    from utils.image_processing import apply_clahe, apply_homomorphic_filter, resize_with_padding
    
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')
    
    # Resize with padding to 144x144 (CNN model was trained with this size)
    image = resize_with_padding(image, target_size=target_size)
    # Ensure grayscale after resize
    if image.mode != 'L':
        image = image.convert('L')
    
    # Gaussian Blur
    img_array = np.array(image)
    img_array = cv2.GaussianBlur(img_array, (3, 3), 0)
    
    # Homomorphic Filter
    image = Image.fromarray(img_array)
    image = apply_homomorphic_filter(image, gamma_h=1.2, gamma_l=0.5, c=1.0, cutoff=30)
    
    # CLAHE
    image = apply_clahe(image)
    
    # Convert to array and normalize
    img_array = np.array(image)
    # Ensure grayscale (should be 2D array)
    if len(img_array.shape) == 3:
        img_array = img_array[:, :, 0]  # Take first channel if RGB somehow
    
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension and channel dimension: (1, 144, 144, 1)
    img_array = np.expand_dims(img_array, axis=0)    # (144, 144) -> (1, 144, 144)
    img_array = np.expand_dims(img_array, axis=-1)   # (1, 144, 144) -> (1, 144, 144, 1)
    
    return img_array


def preprocess_image_with_steps(image, target_size=144):
    """
    Preprocess image and return intermediate steps for visualization
    Pipeline: Grayscale → Resize 144x144 (padding) → Gaussian Blur → Homomorphic Filter → CLAHE → Normalize
    Note: CNN model was trained with 144x144, not 256x256
    
    Returns:
        tuple: (final_array, steps_dict)
        steps_dict contains PIL Images at each preprocessing step
    """
    from utils.image_processing import apply_clahe, apply_homomorphic_filter, resize_with_padding
    
    steps = {}
    
    # Step 1: Original
    steps['original'] = image.copy()
    
    # Step 2: Convert to grayscale
    if image.mode != 'L':
        gray_image = image.convert('L')
    else:
        gray_image = image
    steps['grayscale'] = gray_image.copy()
    
    # Step 3: Resize with padding to 144x144 (CNN model input size)
    resized_image = resize_with_padding(gray_image, target_size=target_size)
    # Ensure grayscale after resize
    if resized_image.mode != 'L':
        resized_image = resized_image.convert('L')
    steps['resized'] = resized_image.copy()
    
    # Step 4: Apply Gaussian Blur 3x3 (SAME AS TRAINING)
    img_array = np.array(resized_image)
    blurred_array = cv2.GaussianBlur(img_array, (3, 3), 0)
    blurred_image = Image.fromarray(blurred_array)
    steps['blurred'] = blurred_image.copy()
    
    # Step 5: Apply Homomorphic Filter with training params (d0=30, gamma_l=0.5, gamma_h=1.2)
    homomorphic_image = apply_homomorphic_filter(blurred_image, gamma_h=1.2, gamma_l=0.5, c=1.0, cutoff=30)
    steps['homomorphic'] = homomorphic_image.copy()
    
    # Step 6: Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe_image = apply_clahe(homomorphic_image)
    steps['clahe'] = clahe_image.copy()
    
    # Step 7: Normalize to [0, 1]
    img_array = np.array(clahe_image)
    # Ensure grayscale (should be 2D array)
    if len(img_array.shape) == 3:
        img_array = img_array[:, :, 0]  # Take first channel if RGB somehow
    
    img_array = img_array.astype('float32') / 255.0
    steps['normalized'] = clahe_image  # Keep PIL format for display
    
    # Add batch and channel dimensions: (1, 144, 144, 1)
    img_array = np.expand_dims(img_array, axis=0)    # (144, 144) -> (1, 144, 144)
    img_array = np.expand_dims(img_array, axis=-1)   # (1, 144, 144) -> (1, 144, 144, 1)
    
    return img_array, steps

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

**Preprocessing Pipeline:** CLAHE + Homomorphic Filtering + Augmentation  
**CNN Model:** Custom architecture (144×144 grayscale) - Accuracy: 99.9%  
**ResNet-50:** Transfer Learning (224×224 RGB, PyTorch) - Đang chuyển đổi sang TensorFlow
""")

# Load models
cnn_model, resnet_model = load_models()

# Store models in session state for Grad-CAM page
if 'cnn_model' not in st.session_state:
    st.session_state.cnn_model = cnn_model
if 'resnet_model' not in st.session_state:
    st.session_state.resnet_model = resnet_model

if not TF_AVAILABLE:
    st.warning("**TensorFlow không khả dụng!** Vui lòng cài đặt: `pip install tensorflow`")
    models_ready = False
elif cnn_model is None:
    if USE_CUSTOM_UI:
        show_info_box("CNN model chưa được load! Kiểm tra file model.", type="error")
    else:
        st.error("CNN model chưa được load! Kiểm tra file model.")
    models_ready = False
else:
    models_ready = True
    if resnet_model is None:
        st.info("**Note:** ResNet model chưa khả dụng (sử dụng PyTorch). Hiện chỉ có CNN model.")

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #0066CC; margin-bottom: 0.5rem;">Cấu hình</h2>
        <p style="color: #666; font-size: 0.9rem;">Model & Settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection
    if resnet_model is None:
        model_choice = st.radio(
            "Chọn model:",
            ["CNN"],
            help="CNN: Custom architecture (Accuracy: 99.9%)"
        )
        st.info("📝 ResNet-50 model đang trong quá trình chuyển đổi từ PyTorch")
    else:
        model_choice = st.radio(
            "Chọn model:",
            ["CNN", "ResNet-50"],
            help="CNN: Custom architecture | ResNet-50: Transfer Learning"
        )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 0.5rem;">
        <h3 style="color: #0066CC; font-size: 1.1rem; margin-bottom: 1rem;">Hướng dẫn sử dụng</h3>
        <div style="padding-left: 1.5rem;">
            <ol style="font-size: 0.9rem; line-height: 1.8; color: #444; margin: 0;">
                <li style="margin-bottom: 0.5rem;">Chọn model (CNN hoặc ResNet-50)</li>
                <li style="margin-bottom: 0.5rem;">Upload ảnh X-quang ngực</li>
                <li style="margin-bottom: 0.5rem;">Xem kết quả phân tích</li>
            </ol>
        </div>
        
        <h3 style="color: #0066CC; font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 1rem;">Team Prompt Engineer</h3>
        <p style="font-size: 0.85rem; line-height: 1.6; color: #666;">
            Nguyễn Văn Quang Duy<br>
            Nguyễn Đặng Quốc Anh<br>
            Nguyễn Đình Tấn Lộc
        </p>
    </div>
    """, unsafe_allow_html=True)

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
            # Preprocess with visualization
            with st.spinner("Đang xử lý ảnh..."):
                processed_image, preprocessing_steps = preprocess_image_with_steps(image)
            
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
            
            # Preprocessing Pipeline Visualization
            st.markdown("---")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white; margin: 1.5rem 0;">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem;">🔬 Preprocessing Pipeline</h3>
                <p style="margin: 0; font-size: 0.95rem; opacity: 0.9;">Xem các bước xử lý ảnh trước khi đưa vào model</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📊 Xem chi tiết từng bước preprocessing", expanded=False):
                st.markdown("""
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
                    Pipeline này áp dụng các kỹ thuật tiền xử lý để tăng chất lượng ảnh và chuẩn hóa input cho model.
                </p>
                """, unsafe_allow_html=True)
                
                # Display steps in a grid (3 columns for compact layout)
                step_info = [
                    ("original", "📷 Original", "Ảnh gốc được upload", "#E3F2FD"),
                    ("grayscale", "⚫ Grayscale", "Convert sang ảnh xám (1 channel)", "#F3E5F5"),
                    ("resized", "🔳 Resize", "Resize về 144×144 pixels với padding (giữ nguyên tỷ lệ)", "#FCE4EC"),
                    ("blurred", "🌫️ Gaussian Blur", "Làm mịn ảnh với kernel 3×3 - Giảm noise", "#E1F5FE"),
                    ("homomorphic", "💡 Homomorphic Filter", "Cân bằng illumination - Loại bỏ ảnh hưởng ánh sáng không đều", "#E8F5E9"),
                    ("clahe", "📈 CLAHE", "Contrast Limited Adaptive Histogram Equalization - Tăng độ tương phản", "#FFF3E0"),
                    ("normalized", "📊 Normalized", "Normalize giá trị pixel về [0, 1] range", "#E0F2F1")
                ]
                
                # Display in 3 columns per row for more compact layout
                for i in range(0, len(step_info), 3):
                    cols = st.columns(3)
                    
                    for idx, col in enumerate(cols):
                        if i + idx < len(step_info):
                            step_key, title, description, bg_color = step_info[i + idx]
                            
                            with col:
                                st.markdown(f"""
                                <div style="background: {bg_color}; padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem; text-align: center;">
                                    <h4 style="margin: 0; color: #333; font-size: 0.9rem;">{title}</h4>
                                    <p style="margin: 0.25rem 0 0 0; color: #666; font-size: 0.75rem; line-height: 1.3;">{description}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if step_key in preprocessing_steps:
                                    # Use fixed width for compact display
                                    st.image(preprocessing_steps[step_key], width=200)
                                else:
                                    st.caption(f"Step {step_key} not available")
                
                # Summary - more compact
                st.markdown("---")
                st.markdown("""
                <div style="background: #F8F9FA; padding: 0.75rem; border-radius: 8px; border-left: 4px solid #0066CC;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #0066CC; font-size: 1rem;">📝 Tóm tắt Pipeline</h4>
                    <p style="margin: 0 0 0.5rem 0; color: #666; font-size: 0.85rem;">
                        Pipeline cho CNN model (input: 144×144)
                    </p>
                    <ol style="margin: 0; padding-left: 1.5rem; line-height: 1.6; color: #444; font-size: 0.85rem;">
                        <li><strong>Grayscale:</strong> RGB → 1 channel</li>
                        <li><strong>Resize:</strong> 144×144 với padding</li>
                        <li><strong>Gaussian Blur:</strong> Giảm noise (3×3)</li>
                        <li><strong>Homomorphic:</strong> Cân bằng ánh sáng (d0=30)</li>
                        <li><strong>CLAHE:</strong> Tăng contrast (clip=2.0)</li>
                        <li><strong>Normalize:</strong> [0,255] → [0,1]</li>
                    </ol>
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
