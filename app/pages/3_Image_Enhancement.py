"""
Image Enhancement Tools Page
"""
import streamlit as st
from PIL import Image
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from utils.image_processing import (
        adjust_brightness,
        adjust_contrast,
        adjust_sharpness,
        apply_clahe,
        apply_homomorphic_filter,
        denoise_image
    )
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

st.set_page_config(
    page_title="Image Enhancement | HCMUTE",
    layout="wide"
)

st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #0066CC 0%, #003d82 100%); 
            color: white; border-radius: 12px; margin-bottom: 2rem;">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Công Cụ Cải Thiện Ảnh</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Tiền xử lý và tối ưu hóa ảnh X-quang</p>
</div>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader(
    "Upload ảnh X-quang",
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None and UTILS_AVAILABLE:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Enhancement Controls")
        
        # Brightness
        brightness = st.slider(
            "Brightness",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust image brightness"
        )
        
        # Contrast
        contrast = st.slider(
            "Contrast",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust image contrast"
        )
        
        # Sharpness
        sharpness = st.slider(
            "Sharpness",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust image sharpness"
        )
        
        # CLAHE
        apply_clahe_check = st.checkbox(
            "Apply CLAHE",
            value=False,
            help="Enhance local contrast (recommended for X-rays)"
        )
        
        # Homomorphic Filter
        apply_homo_check = st.checkbox(
            "Apply Homomorphic Filter",
            value=False,
            help="Normalize illumination (used in training pipeline)"
        )
        
        # Denoise
        denoise_check = st.checkbox(
            "Denoise",
            value=False,
            help="Remove noise from image"
        )
        
        denoise_strength = 10
        if denoise_check:
            denoise_strength = st.slider(
                "Denoise Strength",
                min_value=5,
                max_value=30,
                value=10,
                step=5
            )
        
        # Reset button
        if st.button("Reset to Original"):
            brightness = 1.0
            contrast = 1.0
            sharpness = 1.0
            apply_clahe_check = False
            denoise_check = False
    
    with col2:
        st.subheader("Before & After Comparison")
        
        # Process image
        processed_image = image.copy()
        
        # Apply enhancements
        if brightness != 1.0:
            processed_image = adjust_brightness(processed_image, brightness)
        
        if contrast != 1.0:
            processed_image = adjust_contrast(processed_image, contrast)
        
        if sharpness != 1.0:
            processed_image = adjust_sharpness(processed_image, sharpness)
        
        if apply_clahe_check:
            processed_image = apply_clahe(processed_image)
        
        if apply_homo_check:
            processed_image = apply_homomorphic_filter(processed_image)
        
        if denoise_check:
            processed_image = denoise_image(processed_image, denoise_strength)
        
        # Display side-by-side
        col_before, col_after = st.columns(2)
        
        with col_before:
            st.markdown("**Original**")
            st.image(image, use_container_width=True)
        
        with col_after:
            st.markdown("**Enhanced**")
            st.image(processed_image, use_container_width=True)
        
        # Download button
        st.markdown("---")
        
        # Save enhanced image
        from io import BytesIO
        buf = BytesIO()
        processed_image.save(buf, format='PNG')
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Enhanced Image",
            data=byte_im,
            file_name="enhanced_xray.png",
            mime="image/png"
        )

elif uploaded_file is not None and not UTILS_AVAILABLE:
    st.error("Image processing utilities not available. Please check utils/image_processing.py")

else:
    st.info("Upload ảnh X-quang để bắt đầu enhancement")
    
    # Guide
    st.markdown("---")
    st.subheader("Enhancement Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Brightness
        - Tăng/giảm độ sáng tổng thể
        - Hữu ích cho ảnh quá tối/sáng
        
        ### Contrast
        - Tăng sự khác biệt giữa vùng sáng/tối
        - Làm nổi bật chi tiết
        
        ### Sharpness
        - Tăng độ rõ nét cạnh
        - Cẩn thận: quá sharp → noise
        """)
    
    with col2:
        st.markdown("""
        ### CLAHE
        - Contrast Limited Adaptive Histogram Equalization
        - Tự động cải thiện contrast cục bộ
        - **Rất tốt cho ảnh X-ray**
        
        ### Denoising
        - Loại bỏ noise
        - Làm mượt ảnh
        - Có thể mất chi tiết nhỏ
        """)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                padding: 1.5rem; border-radius: 12px; margin-top: 1rem; border-left: 4px solid #00C853;">
        <h4 style="margin: 0 0 1rem 0; color: #00C853;">Khuyến nghị cho X-ray</h4>
        <ol style="margin: 0; color: #2E7D32; line-height: 1.8;">
            <li>Apply CLAHE để cải thiện contrast</li>
            <li>Light denoising (strength 10-15)</li>
            <li>Slight brightness/contrast adjustment nếu cần</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Enhancement tools help improve X-ray image quality before prediction.")
