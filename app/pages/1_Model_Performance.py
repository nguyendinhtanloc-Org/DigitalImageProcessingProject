"""
Model Performance Dashboard Page
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.visualization import (
    plot_training_history,
    create_comparison_table,
    create_metrics_cards
)

st.set_page_config(
    page_title="Model Performance | HCMUTE",
    layout="wide"
)

st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #0066CC 0%, #003d82 100%); 
            color: white; border-radius: 12px; margin-bottom: 2rem;">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">Hiệu Suất Model</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">So sánh kết quả giữa CNN và ResNet-50</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Training History", "Metrics Comparison", "Confusion Matrix"])

with tab1:
    st.header("Training History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CNN Model")
        
        # Mock training history (replace with actual data)
        cnn_history = {
            'accuracy': [0.75, 0.82, 0.87, 0.90, 0.92],
            'val_accuracy': [0.73, 0.80, 0.85, 0.88, 0.89],
            'loss': [0.55, 0.42, 0.35, 0.28, 0.22],
            'val_loss': [0.58, 0.45, 0.38, 0.32, 0.28]
        }
        
        fig = plot_training_history(cnn_history)
        st.pyplot(fig)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #0066CC;">
            <p style="margin: 0; color: #0066CC; font-weight: 600;">Final Accuracy: 92.0% | Val Accuracy: 89.0%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("ResNet-50 Model")
        
        # Mock training history
        resnet_history = {
            'accuracy': [0.80, 0.88, 0.92, 0.94, 0.95],
            'val_accuracy': [0.78, 0.85, 0.89, 0.91, 0.92],
            'loss': [0.48, 0.35, 0.28, 0.22, 0.18],
            'val_loss': [0.52, 0.40, 0.33, 0.28, 0.25]
        }
        
        fig = plot_training_history(resnet_history)
        st.pyplot(fig)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                    padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #00C853;">
            <p style="margin: 0; color: #00C853; font-weight: 600;">Final Accuracy: 95.0% | Val Accuracy: 92.0%</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("Model Metrics Comparison")
    
    # Mock metrics (replace with actual evaluation results)
    cnn_metrics = {
        'accuracy': 0.89,
        'precision': 0.87,
        'recall': 0.91,
        'f1_score': 0.89
    }
    
    resnet_metrics = {
        'accuracy': 0.92,
        'precision': 0.90,
        'recall': 0.94,
        'f1_score': 0.92
    }
    
    # Display metrics cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CNN Metrics")
        st.markdown(
            create_metrics_cards(
                cnn_metrics['accuracy'],
                cnn_metrics['precision'],
                cnn_metrics['recall'],
                cnn_metrics['f1_score']
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.subheader("ResNet-50 Metrics")
        st.markdown(
            create_metrics_cards(
                resnet_metrics['accuracy'],
                resnet_metrics['precision'],
                resnet_metrics['recall'],
                resnet_metrics['f1_score']
            ),
            unsafe_allow_html=True
        )
    
    # Comparison table
    st.markdown("---")
    st.subheader("Side-by-Side Comparison")
    
    comparison_df = create_comparison_table(cnn_metrics, resnet_metrics)
    
    # Style the dataframe with custom CSS
    def highlight_winner(row):
        return ['background-color: #E3F2FD' if row['Winner'] == 'CNN' else 'background-color: #FFF3E0' for _ in row]
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Conclusion
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                padding: 1.5rem; border-radius: 12px; margin-top: 2rem; border-left: 4px solid #0066CC;">
        <h4 style="margin: 0 0 1rem 0; color: #0066CC;">Kết luận: ResNet-50 vượt trội</h4>
        <ul style="margin: 0; color: #1976D2; line-height: 1.8;">
            <li><strong>Accuracy:</strong> ResNet-50 cao hơn 3%</li>
            <li><strong>Precision:</strong> ResNet-50 cao hơn 3%</li>
            <li><strong>Recall:</strong> ResNet-50 cao hơn 3%</li>
            <li><strong>F1 Score:</strong> ResNet-50 cao hơn 3%</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.header("Confusion Matrix")
    
    col1, col2 = st.columns(2)
    
    def plot_confusion_matrix(cm, title):
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Normal', 'Pneumonia'],
                    yticklabels=['Normal', 'Pneumonia'],
                    ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
        return fig
    
    with col1:
        st.subheader("CNN Confusion Matrix")
        # Mock confusion matrix
        cnn_cm = np.array([[450, 50], [40, 460]])
        fig = plot_confusion_matrix(cnn_cm, "CNN Model")
        st.pyplot(fig)
    
    with col2:
        st.subheader("ResNet-50 Confusion Matrix")
        # Mock confusion matrix
        resnet_cm = np.array([[470, 30], [35, 465]])
        fig = plot_confusion_matrix(resnet_cm, "ResNet-50 Model")
        st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("**Note:** Metrics shown are from test set evaluation. Update với actual results sau khi training.")
