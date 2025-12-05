"""
UI Components and Helper Functions for Streamlit App
"""
import streamlit as st
from pathlib import Path


def load_css():
    """Load custom CSS from static/styles.css"""
    css_file = Path(__file__).parent.parent / "static" / "styles.css"
    
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback inline CSS if file not found
        st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        h1 {
            color: #1e3a8a;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)


def render_header():
    """Render app header with logo"""
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <img src="https://hcmute.edu.vn/Resources/Images/SubDomain/DangNhap/logo_dhsp_01-1.png" alt="HCMUTE Logo">
        </div>
        <h1>Pneumonia Detection from Chest X-Ray</h1>
        <p>Deep Learning Application for Medical Imaging</p>
    </div>
    """, unsafe_allow_html=True)


def render_prediction_card(prediction, confidence, model_name):
    """
    Render prediction result card with modern design
    
    Args:
        prediction (str): "Normal" or "Pneumonia"
        confidence (float): Confidence score (0-100)
        model_name (str): Name of the model used
    """
    css_class = "normal" if prediction.upper() == "NORMAL" else "pneumonia"
    
    st.markdown(f"""
    <div class="prediction-card {css_class}">
        <div class="prediction-label">{prediction.upper()}</div>
        <div class="prediction-model">Model: {model_name}</div>
        <div class="confidence-badge">{confidence:.1f}% Confidence</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render app footer with university info"""
    st.markdown("""
    <div class="footer">
        <h3>Team Prompt Engineer</h3>
        <p>Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh (HCMUTE)</p>
        <p>Môn học: Xử Lý Ảnh Số | Giảng viên: ThS. Đoàn Minh Trí</p>
        <p>Email: <a href="mailto:23133041@student.hcmute.edu.vn">23133041@student.hcmute.edu.vn</a></p>
        <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.8;">Chỉ dùng cho mục đích học tập - Không thay thế chẩn đoán y khoa</p>
    </div>
    """, unsafe_allow_html=True)


def show_info_box(message, type="info"):
    """
    Show styled info/warning box
    
    Args:
        message (str): Message to display
        type (str): "info", "warning", "success", or "error"
    """
    st.markdown(f"""
    <div class="info-box {type}">
        <p style="margin: 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
