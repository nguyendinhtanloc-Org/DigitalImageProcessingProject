"""
Visualization utilities for Streamlit app
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow import keras


def generate_gradcam_heatmap(model, img_array, last_conv_layer_name=None):
    """
    Generate Grad-CAM heatmap for visualization
    
    Args:
        model: Keras model
        img_array: Preprocessed image array
        last_conv_layer_name: Name of last conv layer (auto-detect if None)
    
    Returns:
        heatmap: numpy array of heatmap
    """
    # Auto-detect last conv layer if not specified
    if last_conv_layer_name is None:
        for layer in reversed(model.layers):
            if isinstance(layer, keras.layers.Conv2D):
                last_conv_layer_name = layer.name
                break
    
    # Create a model that maps input to last conv layer + predictions
    grad_model = keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Compute gradient
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]
    
    # Gradient of class score with respect to conv output
    grads = tape.gradient(loss, conv_outputs)
    
    # Pooled gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Weight conv outputs by gradients
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def overlay_heatmap_on_image(image, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap on original image
    
    Args:
        image: PIL Image or numpy array
        heatmap: Grad-CAM heatmap
        alpha: Transparency of heatmap overlay
        colormap: OpenCV colormap
    
    Returns:
        superimposed_img: PIL Image with heatmap overlay
    """
    # Convert PIL to numpy if needed
    if isinstance(image, Image.Image):
        img = np.array(image)
    else:
        img = image
    
    # Resize heatmap to match image
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to RGB
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, colormap)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Superimpose heatmap on image
    superimposed_img = heatmap * alpha + img * (1 - alpha)
    superimposed_img = np.uint8(superimposed_img)
    
    return Image.fromarray(superimposed_img)


def plot_confidence_gauge(confidence, prediction):
    """
    Create a gauge chart for confidence visualization
    
    Args:
        confidence: Confidence score (0-100)
        prediction: "Normal" or "Pneumonia"
    
    Returns:
        fig: Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Colors
    if prediction.lower() == "normal":
        color = '#10b981'  # Green
    else:
        color = '#ef4444'  # Red
    
    # Create gauge
    ax.barh(0, confidence, height=0.5, color=color, alpha=0.8)
    ax.barh(0, 100 - confidence, left=confidence, height=0.5, color='#e5e7eb', alpha=0.5)
    
    # Styling
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Confidence (%)', fontsize=12)
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add text
    ax.text(confidence / 2, 0, f'{confidence:.1f}%', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    plt.tight_layout()
    return fig


def plot_training_history(history_dict):
    """
    Plot training history (accuracy and loss curves)
    
    Args:
        history_dict: Dictionary with 'accuracy', 'val_accuracy', 'loss', 'val_loss'
    
    Returns:
        fig: Matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy
    ax1.plot(history_dict['accuracy'], label='Training', linewidth=2)
    ax1.plot(history_dict['val_accuracy'], label='Validation', linewidth=2)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Loss
    ax2.plot(history_dict['loss'], label='Training', linewidth=2)
    ax2.plot(history_dict['val_loss'], label='Validation', linewidth=2)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def create_comparison_table(cnn_metrics, resnet_metrics):
    """
    Create model comparison table
    
    Args:
        cnn_metrics: Dict with CNN metrics
        resnet_metrics: Dict with ResNet metrics
    
    Returns:
        HTML table string
    """
    html = """
    <table style='width:100%; border-collapse: collapse; margin: 1rem 0;'>
        <thead>
            <tr style='background-color: #f1f5f9;'>
                <th style='padding: 0.75rem; text-align: left; border: 1px solid #e2e8f0;'>Metric</th>
                <th style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0;'>CNN</th>
                <th style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0;'>ResNet-50</th>
                <th style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0;'>Winner</th>
            </tr>
        </thead>
        <tbody>
    """
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    
    for metric, label in zip(metrics, labels):
        cnn_val = cnn_metrics.get(metric, 0)
        resnet_val = resnet_metrics.get(metric, 0)
        winner = 'CNN' if cnn_val > resnet_val else 'ResNet-50'
        winner_class = 'winner-cnn' if cnn_val > resnet_val else 'winner-resnet'
        
        html += f"""
            <tr>
                <td style='padding: 0.75rem; border: 1px solid #e2e8f0;'>{label}</td>
                <td style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0;'>{cnn_val:.2%}</td>
                <td style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0;'>{resnet_val:.2%}</td>
                <td style='padding: 0.75rem; text-align: center; border: 1px solid #e2e8f0; font-weight: 600; color: #0066CC;'>{winner}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    """
    
    return html


def create_metrics_cards(accuracy, precision, recall, f1_score):
    """
    Create HTML cards for metrics display
    
    Args:
        accuracy, precision, recall, f1_score: Float values (0-1)
    
    Returns:
        HTML string with metric cards
    """
    metrics = [
        ('Accuracy', accuracy, '#3b82f6'),
        ('Precision', precision, '#10b981'),
        ('Recall', recall, '#f59e0b'),
        ('F1 Score', f1_score, '#8b5cf6')
    ]
    
    cards_html = "<div style='display: flex; gap: 1rem; margin: 1rem 0;'>"
    
    for name, value, color in metrics:
        cards_html += f"""
        <div style='
            flex: 1;
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {color};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        '>
            <div style='color: #64748b; font-size: 0.875rem; margin-bottom: 0.5rem;'>
                {name}
            </div>
            <div style='color: {color}; font-size: 1.5rem; font-weight: bold;'>
                {value:.2%}
            </div>
        </div>
        """
    
    cards_html += "</div>"
    return cards_html
